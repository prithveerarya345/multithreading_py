import threading
import time
import random

def sequential_quicksort(arr):
    """Traditional single-threaded quicksort implementation"""
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return sequential_quicksort(left) + middle + sequential_quicksort(right)

class ThreadedQuicksort:
    """Class to manage threaded quicksort with a limit on maximum threads"""
    
    def __init__(self, max_threads=8):
        self.max_threads = max_threads
        self.active_threads = 0
        self.thread_lock = threading.Lock()
    
    def sort(self, arr):
        return self._threaded_quicksort(arr)
    
    def _threaded_quicksort(self, arr):
        if len(arr) <= 1:
            return arr
            
        pivot = arr[len(arr) // 2]
        
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        
        can_thread = False
        with self.thread_lock:
            if self.active_threads < self.max_threads:
                self.active_threads += 1
                can_thread = True
        
        left_result = [None]  
        if can_thread and len(left) > 1:
            def sort_left():
                try:
                    left_result[0] = self._threaded_quicksort(left)
                finally:
                    with self.thread_lock:
                        self.active_threads -= 1
            
            left_thread = threading.Thread(target=sort_left)
            left_thread.start()
            
            right_result = self._threaded_quicksort(right)
            
            left_thread.join()
            
            return left_result[0] + middle + right_result
        else:
            return self._threaded_quicksort(left) + middle + self._threaded_quicksort(right)

def benchmark(array_size=100000):
    """Compare performance between threaded and sequential quicksort"""
    test_array = [random.randint(0, 10000) for _ in range(array_size)]
    
    test_array_1 = test_array.copy()
    test_array_2 = test_array.copy()
    
    print(f"Sorting array of size {array_size}...")
    
    start_time = time.time()
    sequential_result = sequential_quicksort(test_array_1)
    sequential_time = time.time() - start_time
    print(f"Sequential quicksort took: {sequential_time:.4f} seconds")
    
    start_time = time.time()
    threaded_sorter = ThreadedQuicksort(max_threads=8)  # Limit to 8 threads
    threaded_result = threaded_sorter.sort(test_array_2)
    threaded_time = time.time() - start_time
    print(f"Threaded quicksort took: {threaded_time:.4f} seconds")
    
    # Verify results match
    print(f"Results match: {sequential_result == threaded_result}")
    
    # Calculate speedup
    if sequential_time > 0:
        speedup = sequential_time / threaded_time
        print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    # Test with different array sizes
    for size in [10000, 100000]:
        benchmark(size)
        print()
