```java
@Configuration
public class DemoApp {

    @Component
    public static class MyBDRPP implements BeanDefinitionRegistryPostProcessor {

        @Override
        public void postProcessBeanDefinitionRegistry(BeanDefinitionRegistry bdr) throws BeansException {

            BeanFactory bf = BeanFactory.class.cast(bdr);

            bdr.registerBeanDefinition("barService",
                    BeanDefinitionBuilder.genericBeanDefinition(BarService.class).getBeanDefinition());

            bdr.registerBeanDefinition("fooService",
                    BeanDefinitionBuilder.genericBeanDefinition(FooService.class,
                            () -> new FooService(bf.getBean(BarService.class))).getBeanDefinition());
        }

        @Override
        public void postProcessBeanFactory(ConfigurableListableBeanFactory configurableListableBeanFactory) throws BeansException {

        }
    }

    public static void main(String[] args) {
        ApplicationContext ac = new AnnotationConfigApplicationContext(DemoApp.class);
        ProgrammaticBeanDefinitionInitializer initializer = new ProgrammaticBeanDefinitionInitializer();
        initializer.initialize((GenericApplicationContext) ac);

    }
}

class FooService {
    private final BarService barService;

    FooService(BarService barService) {
        this.barService = barService;
    }
}

class BarService {}

class ProgrammaticBeanDefinitionInitializer implements ApplicationContextInitializer<GenericApplicationContext> {

    @Override
    public void initialize(GenericApplicationContext genericApplicationContext) {
        genericApplicationContext.registerBean(BarService.class);
        genericApplicationContext.registerBean(FooService.class,
                () -> new FooService(genericApplicationContext.getBean(BarService.class)));

    }
}
```
