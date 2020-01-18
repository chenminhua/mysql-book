go 的 map 不是并发安全的，sync.Map 是并发安全的。

```go
// runtime/map.go
// a header for a Go map.
type hmap struct {
	// Note: the format of the hmap is also encoded in cmd/compile/internal/gc/reflect.go.
	// Make sure this stays in sync with the compiler's definition.
	count     int // # live cells == size of map.  Must be first (used by len() builtin)
	flags     uint8
	B         uint8  // log_2 of # of buckets (can hold up to loadFactor * 2^B items)
	noverflow uint16 // approximate number of overflow buckets; see incrnoverflow for details
	hash0     uint32 // hash seed

	buckets    unsafe.Pointer // array of 2^B Buckets. may be nil if count==0.
	oldbuckets unsafe.Pointer // previous bucket array of half the size, non-nil only when growing
	nevacuate  uintptr        // progress counter for evacuation (buckets less than this have been evacuated)

	extra *mapextra // optional fields
}
```

当然，真正的数据是存在buckets里面的，buckets里面存的是一些bmap的桶。

```go
const (
    // 一个bucket最多放下的key/elem对
    bucketCntBits = 3
    buctetCnt     = 1 << bucketCntBits
)

type bmap struct {
    tophash [bucketCnt]uint8
}
```

在来看创建map的代码

```go
func makemap_small() *hmap {
	h := new(hmap)
	h.hash0 = fastrand()
	return h
}

func makemap(t *maptype, hint int, h *hmap) *hmap {
	.....

	// initialize Hmap
	if h == nil {
		h = (*hmap)(newobject(t.hmap))
	}
	h.hash0 = fastrand()

	// find size parameter which will hold the requested # of elements
	B := uint8(0)
	for overLoadFactor(hint, B) {
		B++
	}
	h.B = B

	......
	return h
}
```

下面来看存和取

```go
func mapaccess1(t *maptype, h *hmap, key unsafe.Pointer) unsafe.Pointer {
    if raceenabled && h != nil {
		callerpc := getcallerpc()
		pc := funcPC(mapaccess1)
		racereadpc(unsafe.Pointer(h), callerpc, pc)
		raceReadObjectPC(t.key, key, callerpc, pc)
	}
	if msanenabled && h != nil {
		msanread(key, t.key.size)
	}
	if h == nil || h.count == 0 {
		if t.hashMightPanic() {
			t.hasher(key, 0) // see issue 23734
		}
		return unsafe.Pointer(&zeroVal[0])
	}
	if h.flags&hashWriting != 0 {
		throw("concurrent map read and map write")
	}
	hash := t.hasher(key, uintptr(h.hash0))
	m := bucketMask(h.B)
	b := (*bmap)(add(h.buckets, (hash&m)*uintptr(t.bucketsize)))
	if c := h.oldbuckets; c != nil {
		if !h.sameSizeGrow() {
			// There used to be half as many buckets; mask down one more power of two.
			m >>= 1
		}
		oldb := (*bmap)(add(c, (hash&m)*uintptr(t.bucketsize)))
		if !evacuated(oldb) {
			b = oldb
		}
	}
	top := tophash(hash)
bucketloop:
	for ; b != nil; b = b.overflow(t) {
		for i := uintptr(0); i < bucketCnt; i++ {
			if b.tophash[i] != top {
				if b.tophash[i] == emptyRest {
					break bucketloop
				}
				continue
			}
			k := add(unsafe.Pointer(b), dataOffset+i*uintptr(t.keysize))
			if t.indirectkey() {
				k = *((*unsafe.Pointer)(k))
			}
			if t.key.equal(key, k) {
				e := add(unsafe.Pointer(b), dataOffset+bucketCnt*uintptr(t.keysize)+i*uintptr(t.elemsize))
				if t.indirectelem() {
					e = *((*unsafe.Pointer)(e))
				}
				return e
			}
		}
	}
	return unsafe.Pointer(&zeroVal[0])
}

```

## sync.Map

runtime/map.go 中的map不是并发安全的，读map的时候会检查hashWriting标志，如果有则报并发错误。

可以用 -race 参数来检查到 map的并发错误。

sync.Map 利用读写锁，而不是Mutex来减少读写时锁带来的性能损失。

但是sync.Map是使用了一把大锁，而java中的ConcurrentHashMap则是采用了分段锁的机制。https://github.com/golang/go/issues/20360 参见这个issue，目前golang还没有计划采用这种方案。
