```java
@EnableBatchProcessing
@SpringBootApplication
public class BatchDemoApp {

    @Data
    @AllArgsConstructor
    @NoArgsConstructor
    public static class Person {
        private int age;
        private String firstName, email;
    }

    @Configuration
    public static class Step1Configuration {

        @Bean
        FlatFileItemReader<Person> fileReader(@Value("${input}") Resource in) throws Exception {

            return new FlatFileItemReaderBuilder<Person>()
                    .name("file-reader")
                    .resource(in)
                    .targetType(Person.class)
                    .delimited().delimiter(",").names(new String[]{"firstName", "age", "email"})
                    .build();
        }

        @Bean
        JdbcBatchItemWriter<Person> jdbcWriter(DataSource ds) {
            return new JdbcBatchItemWriterBuilder<Person>()
                    .dataSource(ds)
                    .sql("insert into PEOPLE( AGE, FIRST_NAME, EMAIL) values (:age, :firstName, :email)")
                    .beanMapped()
                    .build();
        }
    }

    @Configuration
    public static class Step2Configuration {

        @Bean
        ItemReader<Map<Integer, Integer>> jdbcReader(DataSource dataSource) {
            return new JdbcCursorItemReaderBuilder<Map<Integer, Integer>>()
                    .dataSource(dataSource)
                    .name("jdbc-reader")
                    .sql("select COUNT(age) c, age a from PEOPLE group by age")
                    .rowMapper((rs, i) -> Collections.singletonMap(rs.getInt("a"), rs.getInt("c")))
                    .build();
        }

        @Bean
        ItemWriter<Map<Integer, Integer>> fileWriter(@Value("${output}") Resource resource) {
            return new FlatFileItemWriterBuilder<Map<Integer, Integer>>()
                    .name("file-writer")
                    .resource(resource)
                    .lineAggregator(new DelimitedLineAggregator<Map<Integer, Integer>>() {
                        {
                            setDelimiter(",");
                            setFieldExtractor(integerIntegerMap -> {
                                Map.Entry<Integer, Integer> next = integerIntegerMap.entrySet().iterator().next();
                                return new Object[]{next.getKey(), next.getValue()};
                            });
                        }
                    })
                    .build();
        }

    }

    @Bean
    Job job(JobBuilderFactory jbf,
            StepBuilderFactory sbf,
            Step1Configuration step1Configuration,
            Step2Configuration step2Configuration) throws Exception {

        Step s1 = sbf.get("file-db")
                .<Person, Person>chunk(100)
                .reader(step1Configuration.fileReader(null))
                .writer(step1Configuration.jdbcWriter(null))
                .build();

        Step s2 = sbf.get("db-file")
                .<Map<Integer, Integer>, Map<Integer, Integer>>chunk(1000)
                .reader(step2Configuration.jdbcReader(null))
                .writer(step2Configuration.fileWriter(null))
                .build();

        return jbf.get("etl")
                .incrementer(new RunIdIncrementer())
                .start(s1)
                .next(s2)
                .build();

    }

    public static void main(String[] args) {
        System.setProperty("input", "file://" + new File("/Users/jlong/Desktop/in.csv").getAbsolutePath());
        System.setProperty("output", "file://" + new File("/Users/jlong/Desktop/out.csv").getAbsolutePath());

        SpringApplication.run(BatchDemoApp.class, args);
    }
}

```
