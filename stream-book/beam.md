event time vs processing time

windowing: fixed window, sliding window, sessions

### triggers

A trigger is a mechanism for declaring when the output for a window should be materialized relative to some external signal.

Triggers provide flexibility in choosing when outputs should be emitted.

Triggers also make it possible to observe the output for a window multiple times as it evolves.

### watermarks

event time 上的输入完整性。A watermark with value of time X makes the statement: "All input data with event times less than X have been observed"

### accumulation

An accumulation mode specifies the relationship between multiple results that are observed for the same window.

### batch Fundations: what and where

What: Transformations

Beam 里面的两个基本概念： PCollections 和 PTransforms。 PCollections 表示数据集，p 表示 parallel，就是说可以并行处理。PTransforms 表示可以处理并创建新的 PCollections 的操作。

```java

/**

 * counts words in Shakespeare, includes Beam best practices.
 * https://beam.apache.org/get-started/wordcount-example/
 * 读取text文件，然后counting PCollection，然后写入text文件。
 *   1. Executing a Pipeline both locally and using the selected runner
 *   2. Using ParDo with static DoFns defined out-of-line
 *   3. Building a composite transform
 *   4. Defining your own pipeline options
mvn compile exec:java -Dexec.mainClass=org.apache.beam.examples.WordCount \
     -Dexec.args="--inputFile=pom.xml --output=counts" -Pdirect-runner
 */
public class WordCount {

  /**
  This DoFn tokenizes lines of text into individual words; pass to a ParDo in the pipeline.
   */
  static class ExtractWordsFn extends DoFn<String, String> {
    private final Counter emptyLines = Metrics.counter(ExtractWordsFn.class, "emptyLines");
    private final Distribution lineLenDist =
        Metrics.distribution(ExtractWordsFn.class, "lineLenDistro");

    @ProcessElement
    public void processElement(@Element String element, OutputReceiver<String> receiver) {
      lineLenDist.update(element.length());
      if (element.trim().isEmpty()) {
        emptyLines.inc();
      }

      // Split the line into words.
      String[] words = element.split(ExampleUtils.TOKENIZER_PATTERN, -1);

      // Output each word encountered into the output PCollection.
      for (String word : words) {
        if (!word.isEmpty()) {
          receiver.output(word);
        }
      }
    }
  }

  /** A SimpleFunction that converts a Word and Count into a printable string. */
  public static class FormatAsTextFn extends SimpleFunction<KV<String, Long>, String> {
    @Override
    public String apply(KV<String, Long> input) {
      return input.getKey() + ": " + input.getValue();
    }
  }

  /**
   * 用于将lines of text的PCollection转换成word counts结果的PTransform。
   这是一个组合transform，将两个transform (ParDo 和 Count) 组合成一个PTransform */
  public static class CountWords extends PTransform<PCollection<String>,PCollection<KV<String, Long>>> {
    @Override
    public PCollection<KV<String, Long>> expand(PCollection<String> lines) {

      // Convert lines of text into individual words.
      PCollection<String> words = lines.apply(ParDo.of(new ExtractWordsFn()));

      // Count the number of times each word occurs.
      PCollection<KV<String, Long>> wordCounts = words.apply(Count.perElement());

      return wordCounts;
    }
  }

  /** pipeline 的配置 */
  public interface WordCountOptions extends PipelineOptions {

    @Description("Path of the file to read from")
    @Default.String("gs://apache-beam-samples/shakespeare/kinglear.txt")
    String getInputFile();

    void setInputFile(String value);

    /** Set this required option to specify where to write the output. */
    @Description("Path of the file to write to")
    @Required
    String getOutput();

    void setOutput(String value);
  }

  static void runWordCount(WordCountOptions options) {
    Pipeline p = Pipeline.create(options);

    p.apply("ReadLines", TextIO.read().from(options.getInputFile()))
        .apply(new CountWords())
        .apply(MapElements.via(new FormatAsTextFn()))
        .apply("WriteCounts", TextIO.write().to(options.getOutput()));

    p.run().waitUntilFinish();
  }

  public static void main(String[] args) {
    WordCountOptions options =
        PipelineOptionsFactory.fromArgs(args).withValidation().as(WordCountOptions.class);

    runWordCount(options);
  }
}
```

Where: Windowing

Beam provides a unified model that works in both batch and streaming because semantically batch is just a subset of streaming.

### going streaming: When and How

When: Triggers

- Repeated update triggers
- Completeness triggers (watermark)

Repeated update triggers 是 streaming system 中最常见的 trigger。

```java
PCollection<KV<Team, Integer>> totals = input
    .apply(Window.into(FixedWindows.of(TWO_MINUTES))
                  .triggering(Repeatedly(AlignedDelay(TWO_MINUTES))))
    .apply(Sum.integersPerKey())

PCollection<KV<Team, Integer>> totals = input
    .apply(Window.into(FixedWindows.of(TWO_MINUTES))
                  .triggering(Repeatedly(UnalignedDelay(TWO_MINUTES))))
    .apply(Sum.integersPerKey())
```

unaligned delays are typically the better choice for large-scale processing because they result in a more even load distribution over time.

When: Watermarks

```java
PCollection<KV<Team, Integer>> totals = input
    .apply(Window.into(FixedWindows.of(TWO_MINUTES))
                  .triggering(AfterWatermark()))
    .apply(Sum.integersPerKey())
```
