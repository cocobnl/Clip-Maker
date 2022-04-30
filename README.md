# Clip-Maker
Python code that makes the clips out of a video given the markers file exported from Adobe Premiere Pro.\
\
It makes two type of clips:
- Clip made for YouTube: A common clip —trimmed version of the original video— with the same specs as the original. It also writes a txt file with the title of each clip.
- Clip made for IGTV/ TikTok: Vertical clip with the title as header, the original video centered, and the YT Channel banner below it. Some specs might have been changed to the IGTV min specs (fps, for example). It also writes a txt file with the title and the description of each of the clips.*

\* This was made in order to use another Python code to upload those clips with the title and descriptions in its text file.

## Who may be interested?

Initially thinked for podcasters, but also works for streamers, that want to automatize the 'clipification' of their video content and have it organized. Then, it can be used by another code to automatize the uploading in different social media.

## How to use

If first-time user, see [next section](#first-time-adjustments). Then, just run the batch file `ClipMaker.bat` and follow the steps.\
\
![alt text](https://github.com/cocobnl/Clip-Maker/blob/main/clipmaker_image.png?raw=true)

1. Write your podcast/video episode number
2. Write the IG username of your guest (optional)\
A chart is prompted. It shows all of your clips and its specs: title, description, duration.
3. Check if everything is correct. `'y'` (or nothing) to continue, `'n'` to exit, or `'i'` to skip writing YouTube clips and go directly to write IGTV clips.\
YouTube clips will start to be writing, a progress bar is shown.\
After that, IGTV clips will start to be writing. *This takes much more time than the first ones*
4. FINISHED! Press any character to close.

**KEEP AN EYE:** If the length of any clip is under 60 seconds, the IGTV clipification will stop. This is because the IGTV min length for any clip is 60s. However, you can change that modifying the global variable `MIN_LEN`. The same will happen for the case if the description is above the max number of character for IGTV, this is `MAX_CHAR`; however, this case is not usual as the length case.

## First-time adjustments

### Packages
First of all, you have to install the libraries being used, these are: `os`, `sys`, `pandas`, `tqdm`, and `moviepy`. Usually, the installation is easy, however for `moviepy` may require some additional steps. Everything is detailed in the [MoviePy installation guide](https://zulko.github.io/moviepy/install.html). In summary, you just have to install [ImageMagick](https://www.imagemagick.org/script/index.php). **For Windows users, there's an additional step!** You have to provide the path to ImageMagick binary in `moviepy/config_defaults.py` as `IMAGEMAGICK_BINARY = "C:\\Program Files\\ImageMagick_VERSION\\magick.exe"`.

### Directories
After that, open the `ClipMaker.py` file and rewrite some global variables acording to your requirements. First, you should change the 3 first global variables —the directories— as they appear in your PC. These are:
- `MAIN_DIR`. Directory which contains directories of each episode. In my case, `MAIN_DIR = ROOT_DIR\_VIDS`
- `CLIPS_DIR`. Directory which contains the directories YT and IG. In my case, `CLIPS_DIR = ROOT_DIR\CLIPS`
- `BANNER_PATH`. The path of the YouTube Channel banner file. In my case, `BANNER_PATH = ROOT_DIR\Illustr\CSF Frame\Banner IGTV.png`
where for my PC, `ROOT_DIR = C:\Users\jkoki\Documents\COCO\Ciencia Sin Floro`.

**WARNING!** In order for the code to work, the directories must follow a specific order*. For example, for the episode #1. It should be like this:
- Inside the `MAIN_DIR`, there must be a dir named `csf1`, this must contain the video markers named as `csf1.csv`. Also the dir `csf1` must contain a dir named `EXPORTAR AQUI` which contains the original video, the one to be clipped, named as `csf1.mp4`. This is, there must exist these two paths: `MAIN_DIR\csf1\csf1.csv` and `MAIN_DIR\csf1\EXPORTAR AQUI\csf1.mp4`.
- Inside the `CLIPS_DIR`, there must be two dirs `YT` and `IG`, which will contain the clips for YouTube and IGTV respectively. This is, there must exist these two paths: `MAIN_DIR\YT` and `MAIN_DIR\IG`.

\* These directories are also uploaded in the repo in `ROOT_DIR`. They have been uploaded after running the program, so it also contains the clips and respectives txt files. The original video couldn't been uploaded due to its size, however, it can downloaded from [here](https://www.pexels.com/video/ten-minutes-countdown-856925/).

### BAT File
Finally, edit the `ClipMaker.bat` file and replace the path there with the path of your `ClipMaker.py` file.

Now, everything should run. See the steps [above](#how-to-use) to learn how to use it.

### Optional
Additional, you still can make some adjustments for your IGTV Clip design, changing the following global variables in `ClipMaket.py`:
- `BG`. The background color for your clips in RGB format as `(R, G, B)`.
- `FONT`. The font for the titles.
- `SIZE`. The initial size font for your titles. If the title is too long it will be reduces until it fits the video.
- `ZOOM`. The ratio of the video in the clip w.r.t the width of the clip.
