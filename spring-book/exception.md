```java
@ControllerAdvice
public class RestExceptionHandler extends ResponseEntityExceptionHandler {

    @ExceptionHandler({FooException.class})
    protected ResponseEntity<Object> handleFooException(Exception ex, WebRequest req) {
        System.out.println("got it");
        return handleExceptionInternal(ex, "foo foo\n", new HttpHeaders(), HttpStatus.NOT_FOUND, req);
    }

}
```
