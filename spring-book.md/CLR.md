```java
@Component
class SampleMovieCLR implements CommandLineRunner {

    @Autowired
    private MovieRepository movieRepository;

    @Override
    public void run(String... args) throws Exception {
        this.movieRepository.deleteAll();
        Stream.of("Gone with the wind", "the Wizard of Oz", "One Flew over the Cuckoo's Nest")
                .forEach(title -> this.movieRepository.save(new Movie(UUID.randomUUID().toString(), title)));
        this.movieRepository.findByTitle("the Wizard of Oz").thenAccept(System.out::println);
    }
}
```
