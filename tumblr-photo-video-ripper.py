# -*- coding: utf-8 -*-

import os
import sys
import requests
import xmltodict
import urllib
import socket


# Setting timeout
TIMEOUT = 10

# Medium Index Number that Starts from
START = 0

# Numbers of photos/videos per page
MEDIA_NUM = 50


def download_media(site):
    download_photos(site)
    download_videos(site)


def download_videos(site, target_folder=None):
    _download_media(site, "video", START)


def download_photos(site, target_folder=None):
    _download_media(site, "photo", START)


def _download_media(site, medium_type, start):
    current_folder = os.getcwd()
    target_folder = os.path.join(current_folder, site)
    if not os.path.isdir(target_folder):
        os.mkdir(target_folder)

    start = START
    while True:

        base_url = "http://{0}.tumblr.com/api/read?type={1}&num={2}&start={3}"
        media_url = base_url.format(site, medium_type, MEDIA_NUM, start)
        response = requests.get(media_url)
        data = xmltodict.parse(response.content)
        try:
            posts = data["tumblr"]["posts"]["post"]
            for post in posts:
                # select the largest resolution
                # usually in the first element
                medium_url = _handle_medium_url(medium_type, post)
                _download_medium(medium_type, medium_url, target_folder)
            start += 1
        except:
            print("Finish Downloading All the %ss from %s" % (medium_type,
                                                              site))
            break


def _handle_medium_url(medium_type, post):
    if medium_type == "photo":
        return post["photo-url"][0]["#text"]

    if medium_type == "video":
        video_player = post["video-player"][1]["#text"]
        src = video_player.split("\n")[1].split()[1]
        return src.split("=")[1].split("\"")[1]


def _download_medium(medium_type, medium_url, folder_name):
    medium_name = medium_url.split("/")[-1]
    if medium_type == "video":
        if not medium_name.startswith("tumblr"):
            medium_name = medium_url.split("/")[-2]
        medium_name = medium_name + ".mp4"

    file_path = os.path.join(folder_name, medium_name)
    if not os.path.isfile(file_path):
        try:
            socket.setdefaulttimeout(TIMEOUT)
            print("Downloading %s from %s.\n" % (medium_name,
                                                 medium_url))
            urllib.urlretrieve(medium_url, filename=file_path)
        except:
            os.remove(file_path)
            print("Failed to retrieve %s from %s.\n" % (medium_type,
                                                        medium_url))


def usage():
    print 'Please create file sites.txt under this same directory'
    print 'in sites.txt, specify tumblr sites, separated by comma and no space'
    print 'save the file and retry'
    print 'Sample: site1,site2'
    print ''
    print 'Or use command line options'
    print 'Sample: python tumblr-photo-video-ripper.py site1,site2'
    print ''
    print u'未找到sites.txt文件，请创建'
    print u'请在文件中指定Tumblr站点名，并以逗号分割，不要有空格'
    print u'保存文件并重试'
    print u'例子: site1,site2'
    print ''
    print u'或者使用命令行参数指定站点'
    print u'例子: python tumblr-photo-video-ripper.py site1,site2'


if __name__ == "__main__":
    sites = None

    if len(sys.argv) < 2:
        # check the sites file
        filename = 'sites.txt'
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                sites = f.read().rstrip().lstrip().split(',')
        else:
            print usage()
            sys.exit(1)
    else:
        sites = sys.argv[1].split(',')

    if len(sites) == 0 or sites[0] == '':
        print usage()
        sys.exit(1)

    for site in sites:
        download_media(site)
