from pytube import Playlist, YouTube
from tqdm import tqdm
import os
from dotenv import load_dotenv
import re
import subprocess
import time

def sanitize_filename(name):
    # Remove or replace characters that are invalid in file names
    return re.sub(r'[<>:"/\\|?*]', '', name)

def download_playlist(playlist_url, download_path='downloads', resolution='720p', max_retries=5):
    # Create the download directory if it doesn't exist
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    
    playlist = Playlist(playlist_url)
    print(f'Found {len(playlist.video_urls)} videos in the playlist.')

    skipped_videos = []

    for index, video_url in enumerate(tqdm(playlist.video_urls), start=1):
        success = False
        retries = 0

        while not success and retries < max_retries:
            try:
                yt = YouTube(video_url)
                video_stream = yt.streams.filter(res=resolution, file_extension='mp4', only_video=True).first()
                audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()

                if not video_stream or not audio_stream:
                    print(f"Skipping {yt.title}, streams not available.")
                    skipped_videos.append(yt.title)
                    break

                # Format the filename with leading zeros and sanitize it
                sanitized_title = sanitize_filename(yt.title)
                temp_video_file = os.path.join(download_path, f"temp_video_{index:03d}.mp4")
                temp_audio_file = os.path.join(download_path, f"temp_audio_{index:03d}.mp4")
                final_file = os.path.join(download_path, f"{index:03d} - {sanitized_title}.mp4")

                print(f"Downloading video for {sanitized_title}")
                video_stream.download(output_path=download_path, filename=f"temp_video_{index:03d}.mp4")

                print(f"Downloading audio for {sanitized_title}")
                audio_stream.download(output_path=download_path, filename=f"temp_audio_{index:03d}.mp4")

                # Combine video and audio using ffmpeg
                print(f"Combining video and audio for {sanitized_title}")
                command = [
                    'ffmpeg', '-i', temp_video_file, '-i', temp_audio_file, '-c:v', 'copy', '-c:a', 'aac',
                    '-strict', 'experimental', final_file
                ]
                subprocess.run(command, check=True)

                # Remove the temporary files
                os.remove(temp_video_file)
                os.remove(temp_audio_file)

                success = True

            except Exception as e:
                print(f"Error downloading {yt.title}: {e}")
                retries += 1
                if retries < max_retries:
                    print(f"Retrying {yt.title} ({retries}/{max_retries})...")
                    time.sleep(2)  # Sleep for 2 seconds before retrying
                else:
                    print(f"Skipping {yt.title} after {max_retries} failed attempts.")
                    skipped_videos.append(yt.title)

    # Write skipped videos to a text file
    with open('skipped_videos.txt', 'w') as f:
        for title in skipped_videos:
            f.write(f"{title}\n")

if __name__ == "__main__":
    load_dotenv()
    PLAYLIST_URL = os.getenv('PLAYLIST_URL')
    download_playlist(PLAYLIST_URL)
