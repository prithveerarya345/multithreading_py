import threading
import time
import random

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]
    
    left = merge_sort(left)
    right = merge_sort(right)
    
    return merge(left, right)

def merge(left, right):
    merged = []
    left_idx, right_idx = 0, 0
    
    while left_idx < len(left) and right_idx < len(right):
        if left[left_idx] < right[right_idx]:
            merged.append(left[left_idx])
            left_idx += 1
        else:
            merged.append(right[right_idx])
            right_idx += 1
    
    merged.extend(left[left_idx:])
    merged.extend(right[right_idx:])
    
    return merged

def threaded_merge_sort(arr, num_threads=4):
    if len(arr) <= 1:
        return arr
    
    chunk_size = len(arr) // num_threads
    chunks = [arr[i:i + chunk_size] for i in range(0, len(arr), chunk_size)]
    
    threads = []
    sorted_chunks = [[] for _ in range(num_threads)]
    
    def sort_chunk(chunk, index):
        sorted_chunks[index] = merge_sort(chunk)
    
    for i, chunk in enumerate(chunks):
        thread = threading.Thread(target=sort_chunk, args=(chunk, i))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    # Merge all sorted chunks
    result = []
    for chunk in sorted_chunks:
        result = merge(result, chunk)
    
    return result

def test_merge_sort():
    data_size = 10000
    data = [random.randint(0, 100000) for _ in range(data_size)]
    
    print("Single-threaded merge sort:")
    start = time.time()
    sorted_data = merge_sort(data.copy())
    end = time.time()
    print(f"Time taken: {end - start:.4f} seconds")
    
    print("\nMulti-threaded merge sort (4 threads):")
    start = time.time()
    sorted_data_threaded = threaded_merge_sort(data.copy())
    end = time.time()
    print(f"Time taken: {end - start:.4f} seconds")
    
    # Verify both methods produce the same result
    assert sorted_data == sorted_data_threaded
    print("\nBoth methods produced identical sorted results.")

if __name__ == "__main__":
    test_merge_sort()
