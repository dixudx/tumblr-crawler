import os
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
    #download_videos(site)


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


if __name__ == "__main__":
    # tumblr subdomain, e.g. "example1" for "example1.tumblr.com"
    # you can expand the length of sites for your needs
    # sites=["single-site-example"]
    sites = ["example1", "example2", "example3"]
    for site in sites:
        download_media(site)
