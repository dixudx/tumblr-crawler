# -*- coding: utf-8 -*-

import os
import sys
import requests
import xmltodict
import urllib
import socket
from six.moves import queue as Queue
from threading import Thread


# Setting timeout
TIMEOUT = 10

# Retry times
RETRY = 5

# Medium Index Number that Starts from
START = 0

# Numbers of photos/videos per page
MEDIA_NUM = 50

# Numbers of downloading threads concurrently
THREADS = 10


class DownloadWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            medium_type, post, target_folder = self.queue.get()
            self.download(medium_type, post, target_folder)
            self.queue.task_done()

    def download(self, medium_type, post, target_folder):
        try:
            medium_url = self._handle_medium_url(medium_type, post)
            self._download(medium_type, medium_url, target_folder)
        except TypeError:
            pass

    def _handle_medium_url(self, medium_type, post):
        if medium_type == "photo":
            return post["photo-url"][0]["#text"]

        if medium_type == "video":
            video_player = post["video-player"][1]["#text"]
            src = video_player.split("\n")[1].split()[1]
            return src.split("=")[1].split("\"")[1]

    def _download(self, medium_type, medium_url, target_folder):
        socket.setdefaulttimeout(TIMEOUT)
        medium_name = medium_url.split("/")[-1]
        if medium_type == "video":
            if not medium_name.startswith("tumblr"):
                medium_name = medium_url.split("/")[-2]
            medium_name += ".mp4"

        file_path = os.path.join(target_folder, medium_name)
        if not os.path.isfile(file_path):
            print("Downloading %s from %s.\n" % (medium_name,
                                                 medium_url))
            retry_times = 0
            while retry_times < RETRY:
                try:
                    urllib.urlretrieve(medium_url, filename=file_path)
                    break
                except:
                    # try again
                    pass
                retry_times += 1
            else:
                try:
                    os.remove(file_path)
                except OSError:
                    pass
                print("Failed to retrieve %s from %s.\n" % (medium_type,
                                                            medium_url))


class CrawlerScheduler(object):

    def __init__(self, sites):
        self.sites = sites
        self.queue = Queue.Queue()
        self.scheduling()

    def scheduling(self):
        # create workers
        for x in range(THREADS):
            worker = DownloadWorker(self.queue)
            # Setting daemon to True will let the main thread exit
            # even though the workers are blocking
            worker.daemon = True
            worker.start()

        for site in self.sites:
            self.download_media(site)

    def download_media(self, site):
        self.download_photos(site)
        self.download_videos(site)

    def download_videos(self, site):
        self._download_media(site, "video", START)
        # wait for the queue to finish processing all the tasks from one
        # single site
        self.queue.join()
        print("Finish Downloading All the videos from %s" % site)

    def download_photos(self, site):
        self._download_media(site, "photo", START)
        # wait for the queue to finish processing all the tasks from one
        # single site
        self.queue.join()
        print("Finish Downloading All the photos from %s" % site)

    def _download_media(self, site, medium_type, start):
        current_folder = os.getcwd()
        target_folder = os.path.join(current_folder, site)
        if not os.path.isdir(target_folder):
            os.mkdir(target_folder)

        base_url = "http://{0}.tumblr.com/api/read?type={1}&num={2}&start={3}"
        start = START
        while True:
            media_url = base_url.format(site, medium_type, MEDIA_NUM, start)
            response = requests.get(media_url)
            data = xmltodict.parse(response.content)
            try:
                posts = data["tumblr"]["posts"]["post"]
                for post in posts:
                    # select the largest resolution
                    # usually in the first element
                    self.queue.put((medium_type, post, target_folder))
                start += 1
            except:
                break


def usage():
    print("Please create file sites.txt under this same directory")
    print("in sites.txt, specify tumblr sites, separated by comma and no space")
    print("save the file and retry")
    print("Sample: site1,site2")
    print("\n")
    print("Or use command line options")
    print("Sample: python tumblr-photo-video-ripper.py site1,site2")
    print("\n")
    print(u"未找到sites.txt文件，请创建")
    print(u"请在文件中指定Tumblr站点名，并以逗号分割，不要有空格")
    print(u"保存文件并重试")
    print(u"例子: site1,site2")
    print("\n")
    print(u"或者使用命令行参数指定站点")
    print(u"例子: python tumblr-photo-video-ripper.py site1,site2")


if __name__ == "__main__":
    sites = None

    if len(sys.argv) < 2:
        # check the sites file
        filename = "sites.txt"
        if os.path.exists(filename):
            with open(filename, "r") as f:
                sites = f.read().rstrip().lstrip().split(",")
        else:
            print usage()
            sys.exit(1)
    else:
        sites = sys.argv[1].split(",")

    if len(sites) == 0 or sites[0] == "":
        usage()
        sys.exit(1)

    CrawlerScheduler(sites)
