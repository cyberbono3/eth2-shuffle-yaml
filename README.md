# Little Enhancement of eth2-shuffle to shuffle indexs 

Shuffling algorithm for ETH 2.0.

Implemented in four ways:

1. Shuffle elements in array
2. Shuffle individual element (get permuted index)
3. Un-shuffle (i.e. reverse of shuffle effect) elements in array
4. Un-shuffle individual element (get un-permuted index)

Implementation can be found in `shuffle.go`

Note: you can change the hash-function and number of rounds.
Tests use SHA-256 (upcoming in ETH 2.0 spec) and 90 rounds (already a constant).

## Tests

Tests can be found in `shuffle_test.go`.

There are N parallel test cases, generated by code as defined in the spec. Generation code can be found here: `spec/shuffle_test_gen.py`.
Each of these cases as a sub-test for each of the four shuffle-functions mentioned earlier.

## Benchmarks

These benchmarks are ran on a dev-laptop, nothing special.
The primary goal of these benchmarks is to compare per-index shuffling and complete shuffling, not to make it faster than XYZ.
Feel free to run them on your own hardware to compare with your implementations.

With `-test.benchtime=10s`:

```
goos: linux
goarch: amd64
pkg: eth2-shuffle

BenchmarkPermuteIndex/PermuteIndex_4000000-8         	  300000	     49013 ns/op
BenchmarkPermuteIndex/PermuteIndex_40000-8           	  300000	     48936 ns/op
BenchmarkPermuteIndex/PermuteIndex_400-8             	  300000	     48709 ns/op
BenchmarkIndexComparison/Indexwise_ShuffleList_40000-8         	      10	1947872791 ns/op
BenchmarkIndexComparison/Indexwise_ShuffleList_400-8           	    1000	  19435826 ns/op
BenchmarkShuffleList/ShuffleList_4000000-8                     	      10	1253702761 ns/op
BenchmarkShuffleList/ShuffleList_40000-8                       	    1000	  12152166 ns/op
BenchmarkShuffleList/ShuffleList_400-8                         	  100000	    191813 ns/op

```

### `PermuteIndex_X`
Benchmark shuffling of a single item, in a virtual context of `X` items, which are not being shuffled.
Not that the size `X` of the list does not matter much at all,
 it's really just bottlenecked by the performance of shuffling a single index.

### `Indexwise_ShuffleList_X`
Benchmark shuffling of `X` items, but each of them individually using `PermuteIndex`.
Note that there's no `4,000,000` case, it's too inefficient.
Also note that shuffling `40,000` this way, is slower than shuffling a list of 100x the size,
 the efficient way using `ShuffleList`.

### `ShuffleList_X`
Benchmark shuffling of a list of `X` items. (The efficient way, i.e. all simultaneously)


## Contributing

Contributions welcome, please keep the implementation in-line with the ETH 2.0 spec.

## License

MIT, see license file.


