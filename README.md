# Clip-Maker
Python code that makes the clips out of a video given the markers file exported from Adobe Premiere Pro.\
\
It makes two type of clips:
- Clip made for YouTube: A common clip —trimmed version of the original video— with the same specs as the original. It also writes a txt file with the title of each clip.
- Clip made for IGTV/ TikTok: Vertical clip with the title as header, the original video centered, and the YT Channel logo below it. Some specs might have been changed to the IGTV min specs (fps, for example). It also writes a txt file with the title and the description of each of the clips.*

\* This was made in order to use another Python code to upload those clips with the title and descriptions in its text file.

## Who may be interested?

Initially thinked for podcasters, but also works for streamers, that want to automatize the 'clipification' of their video content and have it organized. Then it can be used by another code to automatize the uploading in different social media such.

## How to use it?

Modify the code for your repositories (see next section). Then, just run the batch file `ClipMaker.bat` and follow the steps.
1. Write your podcast/video episode number
2. Write the IG username of your guest (optional)\
A chart is prompted. It shows all of your clips and its specs: title, description, duration.
3. Check if everything is correct. `'y'` (or nothing) to continue, `'n'` to exit, or `'i'` to skip writing YouTube clips and go directly to write IGTV clips.\
YouTube clips will start to be writing, a progress bar is shown.\
After that, IGTV clips will start to be writing. *This takes much more time than the first ones*
4. FINISHED! Press any character to close.

**KEEP AN EYE:** If the length of any clip is under 60 seconds, the IGTV clipification will stop. This is because the IGTV min length for any clip is 60s. However, you can change that modifying the global variable `MIN_LEN`. The same will happen for the case if the description is above the max number of character for IGTV, this is `MAX_CHAR`; however, this case is not usual as the length case.
