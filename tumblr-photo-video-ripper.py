import os
import sys
import time
import requests
import pytumblr
from queue import Queue
from threading import Thread

# Constants
TIMEOUT = 10
MEDIA_NUM = 50
THREADS = 10
DELAY = 1  # Delay in seconds between API requests

# Tumblr API credentials
CONSUMER_KEY = 'YOUR KEY HERE'
CONSUMER_SECRET = 'YOUR SECRET HERE'
OAUTH_TOKEN = 'YOUR OAUTH TOKEN HERE'
OAUTH_SECRET = 'YOUR OAUTH SECRET HERE'

# Initialize the Tumblr client
client = pytumblr.TumblrRestClient(
    CONSUMER_KEY,
    CONSUMER_SECRET,
    OAUTH_TOKEN,
    OAUTH_SECRET
)

class DownloadWorker(Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self):
        while True:
            photo_url, target_folder = self.queue.get()
            self.download(photo_url, target_folder)
            self.queue.task_done()

    def download(self, url, folder):
        try:
            response = requests.get(url, timeout=TIMEOUT)
            if response.status_code == 200:
                filename = os.path.join(folder, os.path.basename(url))
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f"Downloaded: {filename}")
            else:
                print(f"Failed to download {url}")
        except Exception as e:
            print(f"Error downloading {url}: {e}")

class CrawlerScheduler:
    def __init__(self, sites):
        self.sites = sites
        self.queue = Queue()
        self.scheduling()

    def scheduling(self):
        for _ in range(THREADS):
            worker = DownloadWorker(self.queue)
            worker.daemon = True
            worker.start()

        for site in self.sites:
            self.download_media(site)

    def download_media(self, site):
        current_folder = os.getcwd()
        target_folder = os.path.join(current_folder, site.strip())
        os.makedirs(target_folder, exist_ok=True)

        start = 0
        total_downloaded = 0
        while True:
            try:
                posts_data = client.posts(site, type='photo', offset=start, limit=MEDIA_NUM)
                posts = posts_data.get('posts', [])
                
                if not posts:
                    print(f"No more posts found for {site}")
                    break

                num_posts = len(posts)
                print(f"Retrieved {num_posts} posts from {site} starting at offset {start}")

                for post in posts:
                    photo_urls = [photo['original_size']['url'] for photo in post.get('photos', [])]
                    for url in photo_urls:
                        self.queue.put((url, target_folder))

                total_downloaded += num_posts
                start += num_posts

                if num_posts < MEDIA_NUM:
                    print(f"Finished downloading from {site}")
                    break

                time.sleep(DELAY)

            except Exception as e:
                print(f"Error processing posts from {site}: {e}")
                time.sleep(DELAY)  # Retry after delay
                continue

        print(f"Total downloaded from {site}: {total_downloaded}")

def parse_sites(filename):
    with open(filename, "r") as f:
        return [extract_blog_name(site.strip()) for site in f.readlines() if site.strip()]

def extract_blog_name(url):
    return url.split("https://www.tumblr.com/")[1].strip()

if __name__ == "__main__":
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    if len(sys.argv) < 2:
        filename = os.path.join(cur_dir, "sites.txt")
        if os.path.exists(filename):
            sites = parse_sites(filename)
        else:
            print("Please specify sites or create sites.txt.")
            sys.exit(1)
    else:
        sites = [extract_blog_name(url) for url in sys.argv[1].split(",")]

    if not sites:
        print("No valid sites specified.")
        sys.exit(1)

    CrawlerScheduler(sites)
