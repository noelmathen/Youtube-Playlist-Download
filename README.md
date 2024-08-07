# YouTube Playlist Downloader

This Python script downloads all videos from a YouTube playlist and saves them with audio in the specified resolution. It also handles potential download errors, retrying failed downloads up to a specified number of times before skipping and logging the skipped videos.

## Features
- Downloads all videos from a given YouTube playlist URL.
- Saves videos with both video and audio streams in 720p resolution (by default).
- Sanitizes filenames to ensure compatibility with different operating systems.
- Retries failed downloads up to 5 times before skipping.
- Logs skipped videos to a `skipped_videos.txt` file for manual review.

## Requirements

- Python 3.x
- `pytube` library
- `tqdm` library
- `python-dotenv` library
- `ffmpeg` installed on your system

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/YouTube-Playlist-Downloader.git
    cd YouTube-Playlist-Downloader
    ```

2. **Create a virtual environment** (optional but recommended):
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required libraries**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Install ffmpeg**:
    - Follow the installation instructions for your operating system on the [ffmpeg official website](https://ffmpeg.org/download.html).

5. **Create a `.env` file** in the project directory and add your playlist URL:
    ```env
    PLAYLIST_URL="https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID"
    ```

## Usage

Run the script:
```sh
python download.py
