# -*- coding: utf-8 -*-
"""
Python code that makes the clips out of a video given the markers file exported
 from Adobe Premiere Pro.

It makes two type of clips:
- Clip made for YouTube: A common clip —trimmed version of the original video—
  with the same specs as the original. It also writes a txt file with the title
  of each clip.
- Clip made for IGTV/ TikTok: Vertical clip with the title as header, the
  original video centered, and the YT Channel banner below it. Some specs might
  have been changed to the IGTV min specs (fps, for example). It also writes a
  txt file with the title and the description of each of the clips.


Created on Mon Apr  4 21:05:38 2022

@author: coco.bnl
"""

import os
import sys
import pandas as pd
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import TextClip, ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
import moviepy.video.fx.all as vfx
from tqdm import tqdm

# DIRECTORIES

# Directory which contains directories of each episode
MAIN_DIR = r'C:\Users\jkoki\Documents\COCO\Ciencia Sin Floro\_VIDS'
# Directory which contains directories YT and IG
CLIPS_DIR = r'C:\Users\jkoki\Documents\COCO\Ciencia Sin Floro\CLIPS'
# Path of the YouTube Channel banner file
BANNER_PATH = r'C:\Users\jkoki\Documents\COCO\Ciencia Sin Floro\Illustr' \
              r'\CSF Frame\Banner IGTV.png'

# IGTV Clip Design
BG = (25, 16, 26)
FONT = 'Microsoft-YaHei-&-Microsoft-YaHei-UI'
SIZE = 105  # fontsize
ZOOM = 1.2  # Ratio of the video w.r.t the width of the clip.

# IGTV Default Values
MAX_CHAR = 2200
MIN_LEN = 60  # seconds
MIN_FPS = 30
DIM = (1080, 1920)


def query_yes_no(question: str, default: str = 'yes') -> str:
    """
    Ask a yes/no question via input() and return their answer.

    Parameters
    ----------
    question : str
        Question presented to the user.
    default : str, optional
        Presumed answer if the user just hits <Enter>. It must be 'yes',
        'no' or None (meaning an answer is required of the user).
        The default is 'yes'.

    Raises
    ------
    ValueError
        If the default answer is invalid.

    Returns
    -------
    str
        Answer. 1 for 'yes', 0 for 'no', or 2 for 'ig'.

    """

    valid = {'yes': 1, 'y': 1, 'ye': 1,
             'no': 0, 'n': 0,
             'i': 2, 'ig': 2, 'igtv': 2}
    if default is None:
        prompt = ' [y/n] '
    elif default == 'yes':
        prompt = ' [Y/n] '
    elif default == 'no':
        prompt = ' [y/N] '
    else:
        raise ValueError(f'invalid default answer: {default}')

    while True:
        choice = input(question + prompt).lower()
        if default is not None and choice == '':
            return valid[default]
        if choice in valid:
            return valid[choice]
        print("Please respond with 'yes' or 'no' (or 'y' or 'n').")


def prompt_for_inputs() -> tuple[str, str, bool]:
    """
    Reads the inputs for the CSF episode number and the guest ig @username.

    Returns
    -------
    tuple[str, str, bool]
        Tuple with the CSF episode number, ig @username and boolean to check
        if the CSF episode number is in the directories -True for correct,
        False otherwise-

    """

    csf_num = input('Please, write episode number: ')
    ig_account = '@' + input('Please, write guest ig: @')

    # Check if csf_num is correct
    check = True
    markers_path = os.path.join(MAIN_DIR, fr'csf{csf_num}\csf{csf_num}.csv')
    if not os.path.isfile(markers_path):
        check = False
        print('Something is wrong. Check your CSF markers file name'
              ' or its directory name.')

    return csf_num, ig_account, check


def change_dir(csf_num: str) -> tuple[str, str]:
    """
    Changes the current directory (cwd) to the episode directory.

    Parameters
    ----------
    csf_num : str
        CSF episode number.

    Returns
    -------
    tuple[str, str]
        Tuple with the CSF episode directory path and the CSF episode markers
        csv file name.

    """

    markers_path = os.path.join(MAIN_DIR, fr'csf{csf_num}\csf{csf_num}.csv')
    markers_file = os.path.basename(markers_path)
    episode_dir = os.path.dirname(markers_path)  # = 'MAIN_DIR\csf{csf_num}'
    os.chdir(episode_dir)  # Change the cwd

    return episode_dir, markers_file


def read_markers(markers_file: str) -> pd.core.frame.DataFrame:
    """
    Reads, cleans and prints the markers csv file exported from
    Adobe Premiere as a proper dataframe for the clip maker function.

    Parameters
    ----------
    markers_file : str
        The CSF episode markers csv file name.

    Returns
    -------
    markers_df : TYPE
        Dataframe of the markers.

    """

    # Read
    markers_df = pd.read_csv(markers_file, delimiter='\t', encoding='utf-16')

    # Change time format. HH:MM:SS:ff -> HH:MM:SS.ff
    for col in ['In', 'Out']:
        markers_df[col] = markers_df[col].str.replace(':', '.')
        markers_df[col] = markers_df[col].str.replace('.', ':', 2, regex=False)

    # Clean
    markers_df = markers_df.rename(columns={'Marker Name': 'Title'})
    markers_df = markers_df.drop(['Marker Type', 'Unnamed: 6'], axis=1)
    markers_df = markers_df.dropna()
    markers_df = markers_df.reset_index(drop=True)

    # Show
    print()
    print(markers_df.to_markdown())

    return markers_df


def yt_titles(markers_df: pd.core.frame.DataFrame, markers_file: str) -> None:
    """
    Writes a txt file with the titles -in MAYUS- of the clips.

    Parameters
    ----------
    markers_df : pd.core.frame.DataFrame
        The dataframe of the marker.
    markers_file : str
        The CSF episode markers csv file name.

    """

    # Save titles column of the dataframe as a list
    titles, *_ = markers_df.values.T.tolist()

    yt_titles_path = os.path.join(CLIPS_DIR, 'YT',
                                  markers_file.replace('.csv', '_titles.txt'))

    with open(yt_titles_path, 'w') as titles_txt:
        for title in titles:
            titles_txt.write(f'Clip {title.index(title)}\n')
            titles_txt.write(title.upper())
            titles_txt.write('\n'*2)


def yt_clip_maker(markers_df: int, episode_dir: int,
                  markers_file: int) -> None:
    """
    Function that make the clips from the original video.
    It also shows a progress bar.

    Parameters
    ----------
    markers_df : int
        The dataframe of the markers.
    episode_dir : int
        The CSF episode directory path.
    markers_file : int
        The CSF episode markers csv file name.

    """

    # Save each column of the dataframe as a list
    titles, _, intime, outtime, _ = markers_df.values.T.tolist()

    # Two assumptions about the original video
    # 1. Its name is 'csf{csf_num}.mp4'
    # 2. It is inside the directory 'MAIN_DIR\csf{csf_num}\EXPORTAR AQUI'
    vid_path = os.path.join(episode_dir, 'EXPORTAR AQUI',
                            markers_file.replace('.csv', '.mp4'))

    # Render clips
    with tqdm(total=len(titles)) as pbar:
        for i in range(len(titles)):
            pbar.set_description(f'Writing YT Clip {i}')  # Progress Bar

            yt_clip_path = os.path.join(CLIPS_DIR, 'YT',
                                        markers_file.replace('.csv',
                                                             f' c{i}.mp4'))
            with VideoFileClip(vid_path) as video:
                new = video.subclip(intime[i], outtime[i])
                new.write_videofile(yt_clip_path, fps=30, logger=None)
            pbar.update(1)
        pbar.set_description('YT Clips Done')


def igtv_tit_desc(markers_df: pd.core.frame.DataFrame, markers_file: str,
                  ig_account: str) -> None:
    """
    Writes txt files with the title and description of each of the clips.

    Parameters
    ----------
    markers_df : pd.core.frame.DataFrame
        The dataframe of the marker.
    markers_file : str
        The CSF episode markers csv file name.
    ig_account : str
        Guest IG @username.

    """

    # Save titles and description columns of the dataframe as a list
    titles, descriptions, *_ = markers_df.values.T.tolist()

    for i in range(len(titles)):
        # Check description characters limit
        char_num = len(descriptions[i])
        if char_num > MAX_CHAR:
            print(f'Description of clip {i} is too large. Try with '
                  f'{char_num-MAX_CHAR} characters less .')
            sys.exit()

        # Write the file
        igtv_txt_path = os.path.join(CLIPS_DIR, 'IG',
                                     markers_file.replace('.csv',
                                                          f' c{i}.txt'))
        with open(igtv_txt_path, 'w', newline='\n') as clip_txt:
            clip_txt.write(f'{titles[i]}\n{descriptions[i]} {ig_account}')


def igtv_clip_maker(markers_df: int, markers_file: int) -> None:
    """
    Function that make the IGTV clips from the YT clips and the titles.
    It also shows a progress bar.

    Parameters
    ----------
    markers_df : int
        The dataframe of the markers.
    markers_file : int
        The CSF episode markers csv file name.

    """

    # Save title column of the dataframe as a list
    titles, *_ = markers_df.values.T.tolist()

    with tqdm(total=len(titles)) as pbar:
        for i in range(len(titles)):
            pbar.set_description(f'Writing IGTV Clip {i}')  # Progress Bar

            yt_clip_path = os.path.join(CLIPS_DIR, 'YT',
                                        markers_file.replace('.csv',
                                                             f' c{i}.mp4'))
            igtv_clip_path = yt_clip_path.replace('\\YT\\', '\\IG\\')

            with VideoFileClip(yt_clip_path) as clip:

                # Part 1: Video
                # Check IGTV length limit and min FPS
                if clip.duration < MIN_LEN:
                    print(f'Clip {i} is too short. It needs '
                          f'{MIN_LEN-clip.duration} more seconds.')
                    sys.exit()
                if clip.fps < MIN_FPS:
                    print(f'Setting Clip {i} to 30 fps...')
                    clip = clip.set_fps(30)

                clip = clip.fx(vfx.resize, width=ZOOM*1080)
                clip = clip.on_color(size=DIM, color=BG)

                # Part 2: Title
                font_size = SIZE
                title = TextClip(titles[i], fontsize=font_size,
                                 font=FONT, color='white')
                # Adjust title size by width
                while title.w > (clip.w-50):
                    font_size = font_size - 5
                    title = TextClip(titles[i], fontsize=font_size,
                                     font=FONT, color='white')

                title = title.set_position(('center', 0.2), relative=True)
                title = title.set_duration(clip.duration)

                # Part 3: Banner/Logo
                logo = ImageClip(BANNER_PATH)
                logo = logo.set_position(('center', 0.67), relative=True)
                logo = logo.set_duration(clip.duration)

                # Render Clip + Title + Logo
                final_clip = CompositeVideoClip([clip, title, logo])
                final_clip.write_videofile(igtv_clip_path, logger=None)
            pbar.update(1)
        pbar.set_description('IGTV Clips Done')


def main():
    """
    MAIN PROGRAM
    """

    while True:
        csf_num, ig_account, check = prompt_for_inputs()

        if check:
            episode_dir, markers_file = change_dir(csf_num)
            markers_df = read_markers(markers_file)

            ans = query_yes_no('Is everything correct?')
            if ans == 0:
                print('Update your markers csv file and run again, please.\n')
                break
            if ans == 1:
                yt_titles(markers_df, markers_file)
                yt_clip_maker(markers_df, episode_dir, markers_file)
            igtv_tit_desc(markers_df, markers_file, ig_account)
            igtv_clip_maker(markers_df, markers_file)
            break


if __name__ == '__main__':
    main()
