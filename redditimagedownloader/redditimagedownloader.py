#!/usr/bin/env python3
# encoding: utf-8

help_text = """
redditimagedownloader.py - Mass download images on reddit. Choose the minimum karma, the subreddits,
and how many to download. Will also download imgur albums.
Apache License 2.0
Copyright Matthew Livernoche <mattalivernoche@gmail.com>
"""

import sys
import argparse
import urllib.request
import urllib.parse
import json
import os
import imguralbum

def downloadimages(sourceurl, supportedfiletypes, savedir, minimumkarma=1, autodownloadalbums=False, minimum=50, maximum=200, skipafter=10):
    lastthing = ""
    prevlastthing = "dummyvalue"

    # this is the amount of images we have downloaded. this is compared with minimum.
    imagesdownloaded = 0

    # this is the amount of images we have considered downloading.
    imagesconsidered = 0

    while (lastthing != prevlastthing and
           imagesdownloaded < minimum and
           imagesconsidered < maximum and
           imagesconsidered - imagesdownloaded < skipafter):

        newurl = "https://reddit.com/r/{0}/.json?limit=100".format(sourceurl)

        if lastthing:
            newurl = "{0}&after={1}".format(newurl, lastthing)

        requester = urllib.request.Request(url=newurl, headers={'User-Agent':'imagedownloader'})
        response = urllib.request.urlopen(requester)
        jsondata = json.loads(response.read().decode('utf-8'))

        print("Downloading images in {0}".format(newurl))

        for post in jsondata["data"]["children"]:

            if imagesdownloaded >= minimum or imagesconsidered >= maximum or imagesconsidered - imagesdownloaded >= skipafter:
                break

            imageurl = post["data"]["url"]
            imagesconsidered += 1

            if not post["kind"] == "t3":
                print("{0}. No URL in post; skipping.".format(imagesconsidered))
                continue

            if not imageurl.split(":")[0] == "https":
                print("{0}. URL is not secure; skipping.".format(imagesconsidered))
                continue

            if post["data"]["score"] < minimumkarma:
                print("{0}. Score too low; skipping.".format(imagesconsidered))
                continue

            if post["data"]["stickied"] == True:
                print("{0}. Stickied post; skipping.".format(imagesconsidered))
                continue

            file_ext = os.path.splitext(imageurl)[1]
            filename = os.path.basename(imageurl)
            fulldirpath = os.path.join(savedir, post["data"]["subreddit"])
            fullimagepath = os.path.join(fulldirpath, filename)

            if not file_ext in supportedfiletypes and not post["data"]["domain"] == "imgur.com":
                print("{0}. File ext {1} not supported and not an album; skipping.".format(imagesconsidered, file_ext))
                continue

            if not os.path.exists(fulldirpath):
                os.makedirs(fulldirpath)

            if os.path.exists(fullimagepath):
                print("{0}. Image already existed; skipping.".format(imagesconsidered))
                continue
    
            try:
                if post["data"]["domain"] == "imgur.com" and "com" in imageurl.split(".")[-1]:
                    imagesdownloadedfromalbum = 0
                    try:
                        imguralbumdownloader = imguralbum.ImgurAlbumDownloader(imageurl)
                        print("{0}. {2} is an imgur album with image count of {1}.".format(imagesconsidered, imguralbumdownloader.num_images(), imageurl))

                        downloadalbums = autodownloadalbums

                        if autodownloadalbums == False:
                            continue_prompt = input("Continue? y/n")
                            if str(continue_prompt) == "y":
                                downloadalbums = True

                        if downloadalbums:
                            print("{0}. Scanning {1} images from {2}.".format(imagesconsidered, imguralbumdownloader.num_images(), imageurl))
                            imagesdownloadedfromalbum = imguralbumdownloader.save_images(fulldirpath)
                            print("{0}. {1} downloaded from {2}.".format(imagesconsidered, imagesdownloadedfromalbum, imageurl))
                        else:
                            print("{0}. Skipping from prompt.".format(imagesconsidered))

                    except Exception as e:
                        
                        print("Failed to download imgur album for {0}. Error: {1}".format(imageurl, e))
                    
                    imagesdownloaded += imagesdownloadedfromalbum
                else:
                    urllib.request.urlretrieve(imageurl, fullimagepath)
                    print("{0}. ".format(imagesconsidered) + imageurl + " downloaded and saved in " + fullimagepath)
                    imagesdownloaded += 1
                
            except urllib.error.URLError:
                print("{0}. Connection time out. Skipping.".format(imagesconsidered))

        print("Images downloaded: {0}/{1}.".format(imagesdownloaded, minimum))
        prevlastthing = lastthing
        lastthing = post["data"]["name"]


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description=help_text)
    parser.add_argument('--subreddits', nargs='*', help='a list of the subreddits to download from.')
    parser.add_argument('--ext', nargs='*', default=['.jpg', '.png', '.gif', '.jpeg', '.gifv', '.webm', '.mp4'],
                        help='a file types that can be downloaded. they must begin with a period (".").')
    parser.add_argument('--auto', action='store_true', default=False,
                        help='whether or not to download imgur albums automatically.')
    parser.add_argument('--minkarma', type=int, default=1, help='the minimum amount of karma a post must have for it to be downloaded.')
    parser.add_argument('--loc', type=str, help='the directory where files and folders will be saved and created.')
    parser.add_argument('--min', type=int, default=50,
                        help='the minimum target for the amount of images to be downloaded. once this is hit, downloading will stop.')
    parser.add_argument('--max', type=int, default=100,
                        help='the maximum amount of images that will be considered for download. once this is hit, downloading will stop.')
    parser.add_argument('--skipafter', type=int, default=10,
                        help='stop scanning subreddit after we have skipped over so many images.')

    results = parser.parse_args()

    # image source information
    skip = results.skipafter
    minimages = results.min
    maximages = results.max
    autodownload = results.auto
    urllist = results.subreddits
    minkarma = results.minkarma
    supportedfiletypes = results.ext

    # image saving information
    savedir = results.loc

    for url in urllist:
        downloadimages(url, supportedfiletypes, savedir,
                       minimumkarma=minkarma,
                       autodownloadalbums=autodownload,
                       minimum=minimages,
                       maximum=maximages,
                       skipafter=skip)

    sys.exit(0)

