# redditimagedownloader
Mass download images on reddit. Choose the minimum karma, the subreddits, and how many to download. Will also download imgur albums. Written in Python.

# System requirements

You need to have Python3 installed, and python available in your PATH (which most likely already is in your PATH). This may or may not work with Python 2.0+, but it is not tested with that and this script will not target anything below Python 3.0.

# What is this?

This is a Python script with command line support for mass downloading images on reddit. You can specify which subreddits, the extensions you want to download, the minimum amount of karma an image must have to be downloaded, and other options. It also supports downloading imgur albums, which uses a modified version of [imguralbumdownload written by Alex Gisby](https://github.com/alexgisby/imgur-album-downloader).

When images are downloaded, they are saved in a directory specified by the user. Each subreddit is given a subfolder in that directory.

# How to use in command line

```redditimagedownloder``` can be used in the command line. It has the following required parameters:

* ```--subreddits``` - You can provide a list of subreddits, which are seperated by spaces. These should not end with a forward slash, and do not add /r/. Just put the name; for example, ```/r/pics/``` would be wrong, and the correct way would be ```pics```. You can also add ```hot```, ```new```, ```rising```, etc; for example, ```gifs/top``` would fetch the top posts from /r/gifs. However, queries with ? and & do not work.

* ```--loc``` - the path to the folder where images will be saved. As stated above, subreddits are each given a subfolder in this directory.

There are also these optional parameters:

* ```--ext``` - These file extensions the script can download. This is a whitelist, which means that anything not on this list will not be downloaded. The following extensions are the default: .jpg, .png, .gif, .jpeg, .gifv, .webm, and .mp4. When defining your own list, you must start the extension with a period and they must be seperated by spaces.

* ```--auto``` - When downloading imgur albums, you can add this to make downloading automatic; otherwise, the script will ask if you want to download the album (and it will tell you how many images are in the album). The default is not enabled; to enable, simply add ```--auto```.

* ```--minkarma``` - The minimum amount of karma a post should have for it to be downloaded; anything lower will be skipped. The default is 1. This was added to avoid downloading images that have negative karma.

* ```--min``` - The minimum amount of images that you want to download (including the number of images in an album). Once this number is reached, the script will stop.

* ```--max``` - The maximum amount of images that the script will look at. This is NOT the maximum amount of images downloaded, because the script will stop downloading when ```--min``` is reached.

* ```--skipafter``` - this will tell the script to stop after it has skipped over a certain number of images. This was added mostly for slow moving subreddits, which are updated less often. For example, if the script is looking at such a subreddit and it has downloaded the 200 most recently added images, the script won't look at all 200; it will look at ```--skipafter``` amount and then stop scanning the subreddit.

# How to save settings

This script won't save settings. It simply parses the command line arguments; however, you don't have to enter your desired arguments every single time. On Windows, You can easily save arguments with a ```.bat``` file. Here is an example:

```py redditimagedownloader.py --subreddits pics gifs --loc D:\Gallery\downloads --min 100 --max 200 --minkarma 1 --auto --ext .jpg .png .gif .jpeg```

If you want the window to stay open, you can also do:

```cmd /k py redditimagedownloader.py --subreddits pics gifs --loc D:\Gallery\downloads --min 100 --max 200 --minkarma 1 --auto --ext .jpg .png .gif .jpeg```

Write your desired command in a blank file in your favorite text editor (Notepad is fine) and save it as a ```.bat``` file.
