# -*- coding: utf-8 -*-

import os
import sys
import requests
import xmltodict
from six.moves import queue as Queue
from threading import Thread
import re
import json


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


def video_hd_match():
    hd_pattern = re.compile(r'.*"hdUrl":("([^\s,]*)"|false),')

    def match(video_player):
        hd_match = hd_pattern.match(video_player)
        try:
            if hd_match is not None and hd_match.group(1) != 'false':
                return hd_match.group(2).replace('\\', '')
        except:
            return None
    return match


def video_default_match():
    default_pattern = re.compile(r'.*src="(\S*)" ', re.DOTALL)

    def match(video_player):
        default_match = default_pattern.match(video_player)
        if default_match is not None:
            try:
                return default_match.group(1)
            except:
                return None
    return match


class DownloadWorker(Thread):
    def __init__(self, queue, proxies=None):
        Thread.__init__(self)
        self.queue = queue
        self.proxies = proxies
        self._register_regex_match_rules()

    def run(self):
        while True:
            medium_type, post, target_folder = self.queue.get()
            self.download(medium_type, post, target_folder)
            self.queue.task_done()

    def download(self, medium_type, post, target_folder):
        try:
            medium_url = self._handle_medium_url(medium_type, post)
            if medium_url is not None:
                self._download(medium_type, medium_url, target_folder)
        except TypeError:
            pass

    # can register differnet regex match rules
    def _register_regex_match_rules(self):
        # will iterate all the rules
        # the first matched result will be returned
        self.regex_rules = [video_hd_match(), video_default_match()]

    def _handle_medium_url(self, medium_type, post):
        try:
            if medium_type == "photo":
                return post["photo-url"][0]["#text"]

            if medium_type == "video":
                video_player = post["video-player"][1]["#text"]
                for regex_rule in self.regex_rules:
                    matched_url = regex_rule(video_player)
                    if matched_url is not None:
                        return matched_url
                else:
                    raise Exception
        except:
            raise TypeError("Unable to find the right url for downloading. "
                            "Please open a new issue on "
                            "https://github.com/dixudx/tumblr-crawler/"
                            "issues/new attached with below information:\n\n"
                            "%s" % post)

    def _download(self, medium_type, medium_url, target_folder):
        medium_name = medium_url.split("/")[-1].split("?")[0]
        if medium_type == "video":
            if not medium_name.startswith("tumblr"):
                medium_name = "_".join([medium_url.split("/")[-2],
                                        medium_name])

            medium_name += ".mp4"
            medium_url = 'https://vt.tumblr.com/' + medium_name

        file_path = os.path.join(target_folder, medium_name)
        if not os.path.isfile(file_path):
            print("Downloading %s from %s.\n" % (medium_name,
                                                 medium_url))
            retry_times = 0
            while retry_times < RETRY:
                try:
                    resp = requests.get(medium_url,
                                        stream=True,
                                        proxies=self.proxies,
                                        timeout=TIMEOUT)
                    if resp.status_code == 403:
                        retry_times = RETRY
                        print("Access Denied when retrieve %s.\n" % medium_url)
                        raise Exception("Access Denied")
                    with open(file_path, 'wb') as fh:
                        for chunk in resp.iter_content(chunk_size=1024):
                            fh.write(chunk)
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

    def __init__(self, sites, proxies=None):
        self.sites = sites
        self.proxies = proxies
        self.queue = Queue.Queue()
        self.scheduling()

    def scheduling(self):
        # create workers
        for x in range(THREADS):
            worker = DownloadWorker(self.queue,
                                    proxies=self.proxies)
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

        base_url = "https://{0}.tumblr.com/api/read?type={1}&num={2}&start={3}"
        start = START
        while True:
            media_url = base_url.format(site, medium_type, MEDIA_NUM, start)
            response = requests.get(media_url,
                                    proxies=self.proxies)
            if response.status_code == 404:
                print("Site %s does not exist" % site)
                break

            try:
                xml_cleaned = re.sub(u'[^\x20-\x7f]+',
                                     u'', response.content.decode('utf-8'))
                data = xmltodict.parse(xml_cleaned)
                posts = data["tumblr"]["posts"]["post"]
                for post in posts:
                    try:
                        # if post has photoset, walk into photoset for each photo
                        photoset = post["photoset"]["photo"]
                        for photo in photoset:
                            self.queue.put((medium_type, photo, target_folder))
                    except:
                        # select the largest resolution
                        # usually in the first element
                        self.queue.put((medium_type, post, target_folder))
                start += MEDIA_NUM
            except KeyError:
                break
            except UnicodeDecodeError:
                print("Cannot decode response data from URL %s" % media_url)
                continue
            except:
                print("Unknown xml-vulnerabilities from URL %s" % media_url)
                continue


def usage():
    print("1. Please create file sites.txt under this same directory.\n"
          "2. In sites.txt, you can specify tumblr sites separated by "
          "comma/space/tab/CR. Accept multiple lines of text\n"
          "3. Save the file and retry.\n\n"
          "Sample File Content:\nsite1,site2\n\n"
          "Or use command line options:\n\n"
          "Sample:\npython tumblr-photo-video-ripper.py site1,site2\n\n\n")
    print(u"未找到sites.txt文件，请创建.\n"
          u"请在文件中指定Tumblr站点名，并以 逗号/空格/tab/表格鍵/回车符 分割，支持多行.\n"
          u"保存文件并重试.\n\n"
          u"例子: site1,site2\n\n"
          u"或者直接使用命令行参数指定站点\n"
          u"例子: python tumblr-photo-video-ripper.py site1,site2")


def illegal_json():
    print("Illegal JSON format in file 'proxies.json'.\n"
          "Please refer to 'proxies_sample1.json' and 'proxies_sample2.json'.\n"
          "And go to http://jsonlint.com/ for validation.\n\n\n")
    print(u"文件proxies.json格式非法.\n"
          u"请参照示例文件'proxies_sample1.json'和'proxies_sample2.json'.\n"
          u"然后去 http://jsonlint.com/ 进行验证.")


def parse_sites(filename):
    with open(filename, "r") as f:
        raw_sites = f.read().rstrip().lstrip()

    raw_sites = raw_sites.replace("\t", ",") \
                         .replace("\r", ",") \
                         .replace("\n", ",") \
                         .replace(" ", ",")
    raw_sites = raw_sites.split(",")

    sites = list()
    for raw_site in raw_sites:
        site = raw_site.lstrip().rstrip()
        if site:
            sites.append(site)
    return sites


if __name__ == "__main__":
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    sites = None

    proxies = None
    proxy_path = os.path.join(cur_dir, "proxies.json")
    if os.path.exists(proxy_path):
        with open(proxy_path, "r") as fj:
            try:
                proxies = json.load(fj)
                if proxies is not None and len(proxies) > 0:
                    print("You are using proxies.\n%s" % proxies)
            except:
                illegal_json()
                sys.exit(1)

    if len(sys.argv) < 2:
        # check the sites file
        filename = os.path.join(cur_dir, "sites.txt")
        if os.path.exists(filename):
            sites = parse_sites(filename)
        else:
            usage()
            sys.exit(1)
    else:
        sites = sys.argv[1].split(",")

    if len(sites) == 0 or sites[0] == "":
        usage()
        sys.exit(1)

    CrawlerScheduler(sites, proxies=proxies)
