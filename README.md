## Task 1: Multi-threaded Merge Sort

The implementation uses a data-parallel approach to merge sort by:
1. Dividing the input array into equal-sized chunks
2. Sorting each chunk in a separate thread using the regular merge sort algorithm
3. Merging all the sorted chunks back together

### Code Structure:
- `merge_sort()`: Standard recursive merge sort implementation
- `merge()`: Helper function to merge two sorted arrays
- `threaded_merge_sort()`: Divides data into chunks and uses threads to sort them
- `test_merge_sort()`: Benchmarks and compares both implementations

### Usage:
```
python q1_merge.py
```

The script will display timing information comparing single-threaded vs. multi-threaded performance.

### Sample Output:
```
Single-threaded merge sort:
Time taken: 0.0576 seconds

Multi-threaded merge sort (4 threads):
Time taken: 0.0321 seconds

Both methods produced identical sorted results.
```

## Task 2: Multi-threaded Quicksort

The quicksort implementation uses threads to sort partitions concurrently, with a limit on the maximum number of threads to avoid resource exhaustion.

### Usage:
```
python q2_quicksort.py
```

## Task 3: Concurrent File Downloader

The file downloader uses threads to download multiple files simultaneously.

### Usage:
```
# Download files from command line URLs
python q3_downloader.py --urls http://example.com/file1.txt http://example.com/file2.jpg --output downloads --threads 5

# Download files from a text file containing URLs
python q3_downloader.py --file urls.txt --output downloads --threads 5
```

## Notes on Python Threading Performance

For CPU-bound tasks like sorting, Python's Global Interpreter Lock (GIL) can limit the performance benefits of threading. The GIL prevents multiple threads from executing Python bytecode simultaneously, which means threads can't truly run in parallel for CPU-intensive operations.

Performance improvements are typically seen when:
1. The problem size is large enough that threading overhead is offset by parallel execution
2. The task involves I/O operations (like file downloading) where threads can wait independently
