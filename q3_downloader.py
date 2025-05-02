import threading
import time
import os
import requests
import argparse
from urllib.parse import urlparse

def download_file(url, output_dir="."):
    """Download a file from a URL and save it to the specified directory"""
    # Extract filename from URL
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    
    # Use a default name if path is empty
    if not filename:
        filename = f"downloaded_file_{hash(url) % 10000}"
    
    # Create the full path
    output_path = os.path.join(output_dir, filename)
    
    try:
        # Send HTTP request
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()  # Raise exception for bad status codes
        
        # Get file size if available
        file_size = int(response.headers.get('Content-Length', 0))
        
        # Save the file
        with open(output_path, 'wb') as f:
            if file_size > 0:
                # Show progress for larger files
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
            else:
                # Small file or unknown size
                f.write(response.content)
                
        print(f"Downloaded: {url} -> {output_path}")
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def sequential_download(urls, output_dir="."):
    """Download files sequentially"""
    results = []
    
    start_time = time.time()
    for url in urls:
        result = download_file(url, output_dir)
        results.append(result)
    total_time = time.time() - start_time
    
    successful = results.count(True)
    print(f"\nSequential download complete!")
    print(f"Downloaded {successful} of {len(urls)} files in {total_time:.2f} seconds")
    return total_time

def threaded_download(urls, output_dir=".", max_threads=5):
    """Download files using multiple threads"""
    threads = []
    results = [False] * len(urls)
    
    # Function for thread to execute
    def download_worker(index, url):
        results[index] = download_file(url, output_dir)
    
    start_time = time.time()
    
    # Create and start threads
    for i, url in enumerate(urls):
        thread = threading.Thread(target=download_worker, args=(i, url))
        threads.append(thread)
        thread.start()
        
        # Limit number of concurrent threads
        if len(threads) >= max_threads:
            # Wait for a thread to complete before creating more
            threads[0].join()
            threads.pop(0)
    
    # Wait for remaining threads to complete
    for thread in threads:
        thread.join()
        
    total_time = time.time() - start_time
    
    successful = results.count(True)
    print(f"\nThreaded download complete!")
    print(f"Downloaded {successful} of {len(urls)} files in {total_time:.2f} seconds")
    return total_time

def load_urls_from_file(file_path):
    """Load URLs from a text file, one URL per line"""
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def main():
    parser = argparse.ArgumentParser(description="Concurrent File Downloader")
    
    # Add command line arguments
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--urls', nargs='+', help='List of URLs to download')
    group.add_argument('--file', help='Text file containing URLs (one per line)')
    
    parser.add_argument('--output', default='downloads', 
                      help='Directory to save downloaded files (default: downloads)')
    parser.add_argument('--threads', type=int, default=5,
                      help='Maximum number of concurrent download threads (default: 5)')
    
    args = parser.parse_args()
    
    # Get URLs from command line or file
    if args.urls:
        urls = args.urls
    else:
        urls = load_urls_from_file(args.file)
    
    # Create output directory if it doesn't exist
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    
    print(f"Preparing to download {len(urls)} files")
    
    # Run sequential download
    print("\n=== Sequential Download ===")
    seq_time = sequential_download(urls, args.output)
    
    # Run threaded download
    print("\n=== Threaded Download ===")
    thread_time = threaded_download(urls, args.output, args.threads)
    
    # Compare performance
    if seq_time > 0:
        speedup = seq_time / thread_time
        print(f"\nPerformance comparison:")
        print(f"Sequential: {seq_time:.2f} seconds")
        print(f"Threaded: {thread_time:.2f} seconds")
        print(f"Speedup: {speedup:.2f}x")

# Optional challenge using ThreadPoolExecutor
def download_with_thread_pool(urls, output_dir=".", max_workers=5):
    """Download files using ThreadPoolExecutor"""
    from concurrent.futures import ThreadPoolExecutor
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all download tasks
        future_to_url = {
            executor.submit(download_file, url, output_dir): url for url in urls
        }
        
        # Process results as they complete
        results = []
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"Error processing {url}: {e}")
                results.append(False)
    
    total_time = time.time() - start_time
    successful = results.count(True)
    
    print(f"\nThreadPool download complete!")
    print(f"Downloaded {successful} of {len(urls)} files in {total_time:.2f} seconds")
    return total_time

if __name__ == "__main__":
    main()
