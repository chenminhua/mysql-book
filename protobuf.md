# proto2

## define a message type

```protobuf
message SearchRequest {
  required string query = 1;
  optional int32 page_number = 2;
  optional int32 result_per_page = 3;
}
```

unique numbered tag是用于唯一标识你的字段的，一旦开始用就不能变了。最小为1,最大为2^29 - 1

reserved fileds  保留字段和tag

## optional fields and default values  

```
optional int32 result_per_page = 3 [default = 10];
```

## 枚举类型

```
enum Corpus {
  UNIVERSAL = 0;
  WEB = 1;
  IMAGES = 2;
  LOCAL = 3;
  NEWS = 4;
  PRODUCTS = 5;
  VIDEO = 6;
}
optional Corpus corpus = 4 [default = UNIVERSAL];
```

## nested types
```
message SearchResponse {
  message Result {
    required string url = 1;
    optional string title = 2;
    repeated string snippets = 3;
  }
  repeated Result result = 1;
}
```

## updating a message type
new fields should be optional or repeated.
reserve non-required fields' tags when remove them.

## extensions
```
message Foo {
  extension 100 to 199; // 100 到 199被保留了
}

extend Foo {
  optional int32 bar = 126;   // 扩展这个message
}
```

## oneof 只有一个有效
```
message SampleMessage {
  oneof test_oneof {
    string name = 4;
    SubMessage sub_message = 9;
  }
}
```

## maps
```
map<string, Project> projects = 3;
```

## packages
```
package foo.Bar
message Open { ... }


message Foo {
  required foo.bar.Open open = 1;
}
```

## services
```
service SearchService {
  rpc Search (SearchRequest) returns (SearchResponse);
}
```

## options


# proto3
去掉了required字段，去掉了default value (why)，去掉了extension

增加了 any.proto, empty.proto, timestamp.proto, duration.proto
