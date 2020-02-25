“A Stream is a tool for building up complex operations on collections using a functional approach.”

```java
int londonArtistCount = allArtists.stream().filter(artist -> artist.isFrom(“London”)).count();
```
