import urllib.request
import urllib.parse
import json
import os
import imguralbum

def downloadimages(sourceurl, supportedfiletypes, savedir, minimumkarma=1, autodownloadalbums=False, minimum=50, maximum=200):
    def downloadimguralbum(albumurl, imageid, downloaddirpath):
        try:
            imguralbumdownloader = imguralbum.ImgurAlbumDownloader(albumurl)
            print("{0}. {2} is an imgur album with image count of {1}. Album can be downloaded using imguralbum.py.".format(imageid, imguralbumdownloader.num_images(), albumurl))

            downloadalbums = autodownloadalbums

            if autodownloadalbums == False:
                continue_prompt = input("Continue? y/n")
                if str(continue_prompt) == "y":
                    downloadalbums = True

            if downloadalbums:
                print("{0}. Downloading {1} images.".format(imageid, imguralbumdownloader.num_images()))
                imguralbumdownloader.save_images(downloaddirpath)
            else:
                print("{0}. Skipping.".format(imageid))

        except Exception as e:
            print("Failed to download imgur album for {0}.".format(albumurl))

    def downloadregularimage(imageurl, imagecount, fullimagepath):
        urllib.request.urlretrieve(imageurl, fullimagepath)
        print("{0}. ".format(imagecount) + imageurl + " downloaded and saved in " + fullimagepath)

    lastthing = ""

    # this is the amount of images we have downloaded. this is compared with minimum.
    imagesdownloaded = 0

    # this is the amount of images we have considered downloading.
    imagesconsidered = 0

    while imagesdownloaded < minimum and imagesconsidered < maximum:

        newurl = "https://reddit.com/r/{0}/.json?limit=100".format(sourceurl)

        if lastthing:
            newurl = "{0}&after={1}".format(newurl, lastthing)

        requester = urllib.request.Request(url=newurl, headers={'User-Agent':'imagedownloader'})
        response = urllib.request.urlopen(requester)
        jsondata = json.loads(response.read().decode('utf-8'))

        print("Downloading images in {0}".format(newurl))

        for post in jsondata["data"]["children"]:

            if imagesdownloaded >= minimum or imagesconsidered >= maximum:
                break

            imageurl = post["data"]["url"]
            imagesconsidered += 1

            if not post["kind"] == "t3":
                print("{0}. No URL in post; skipping.".format(imagesconsidered))
                continue

            if not imageurl.split(":")[0] == "https":
                print("{0}. URL is not secure; skipping.".format(imagesconsidered))
                continue

            file_ext = os.path.splitext(imageurl)[1]
            filename = os.path.basename(imageurl)
            fulldirpath = os.path.join(savedir, post["data"]["subreddit"])
            fullimagepath = os.path.join(fulldirpath, filename)

            if not file_ext in supportedfiletypes:

                # check to see if it is an imgur album.
                if post["data"]["domain"] == "imgur.com" and "com" in imageurl.split(".")[-1]:
                    try:
                        imguralbumdownloader = imguralbum.ImgurAlbumDownloader(imageurl)
                        print("{0}. {2} is an imgur album with image count of {1}. Album can be downloaded using imguralbum.py.".format(imagesconsidered, imguralbumdownloader.num_images(), imageurl))

                        downloadalbums = autodownloadalbums

                        if autodownloadalbums == False:
                            continue_prompt = input("Continue? y/n")
                            if str(continue_prompt) == "y":
                                downloadalbums = True

                        if downloadalbums:
                            print("{0}. Downloading {1} images.".format(imagesconsidered, imguralbumdownloader.num_images()))
                            imguralbumdownloader.save_images(fulldirpath)
                        else:
                            print("{0}. Skipping.".format(imagesconsidered))

                    except Exception as e:
                        print("Failed to download imgur album for {0}.".format(imageurl))
                else:
                    print("{0}. File ext {1} not supported; skipping.".format(imagesconsidered, file_ext))

                continue

            if post["data"]["score"] < minimumkarma:
                print("{0}. Score too low; skipping.".format(imagesconsidered))
                continue

            if post["data"]["stickied"] == True:
                print("{0}. Stickied post; skipping.".format(imagesconsidered))
                continue

            if not os.path.exists(fulldirpath):
                os.makedirs(fulldirpath)

            if os.path.exists(fullimagepath):
                print("{0}. Image already existed; skipping.".format(imagesconsidered))
                continue
    
            try:
                if post["data"]["domain"] == "imgur.com" and "com" in imageurl.split(".")[-1]:
                    downloadimguralbum(imageurl, imagesconsidered, fulldirpath)
                else:
                    downloadregularimage(imageurl, imagesconsidered, fullimagepath)
                
                imagesdownloaded += 1
            except urllib.error.URLError:
                print("Connection time out. Skipping.")
        print("Images downloaded: {0}/{1}.".format(imagesdownloaded, minimum))
        lastthing = post["data"]["name"]


if __name__ == "__main__":
    # image source information
    minkarma = 1
    supportedfiletypes = ['.jpg', '.png', '.gif', '.jpeg']

    # image saving information
    savedir = "D:\\Gallery\\downloads"

    urllist = [
        #"ecchi",
        #"thighdeology",
        #"animelegwear",
        #"ZettaiRyouiki",
        #"animelegs",
        #"animeponytails",
        #"kitsunemimi",
        #"onetruebiribiri",
        "reiayanami",
        #"awwnime",
        #"OneTrueUiharu",
        #"tyingherhairup"
        ]

    for url in urllist:
        downloadimages(url, supportedfiletypes, savedir, minimumkarma=minkarma, autodownloadalbums=True, minimum=200, maximum=500)

