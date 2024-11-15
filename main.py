import os
import tkinter as tk
from tkinter import messagebox
from pytube import Channel, YouTube
from pydub import AudioSegment
from threading import Thread

# Function to download and convert a video to MP3
def download_video_as_mp3(video_url, output_folder):
    try:
        # Download the audio stream
        yt = YouTube(video_url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        if audio_stream is None:
            print(f"No audio stream available for {video_url}")
            return

        # Save audio stream as .mp4 (temporary file)
        temp_filename = audio_stream.download(output_folder)
        base, _ = os.path.splitext(temp_filename)
        mp3_filename = f"{base}.mp3"

        # Convert to .mp3 format using pydub
        audio = AudioSegment.from_file(temp_filename)
        audio.export(mp3_filename, format="mp3")
        os.remove(temp_filename)  # Clean up .mp4 file

        print(f"Downloaded and converted to MP3: {mp3_filename}")
    except Exception as e:
        print(f"Failed to download {video_url}: {e}")

# Main function to download all videos as MP3 from a channel
def download_channel_mp3(channel_url, output_folder="downloaded_mp3"):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get all video URLs from the channel
    try:
        channel = Channel(channel_url)
        print(f"Found {len(channel.video_urls)} videos in the channel.")

        # Download each video as MP3
        for video_url in channel.video_urls:
            download_video_as_mp3(video_url, output_folder)
        messagebox.showinfo("Success", "All videos have been downloaded as MP3!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to retrieve channel: {e}")

# Function to start the download in a separate thread
def start_download():
    channel_url = url_entry.get().strip()
    if not channel_url:
        messagebox.showwarning("Input Error", "Please enter a YouTube channel URL.")
        return

    # Run the download process in a separate thread to avoid freezing the GUI
    Thread(target=download_channel_mp3, args=(channel_url,)).start()

# Set up the GUI
root = tk.Tk()
root.title("YouTube Channel to MP3 Downloader")
root.geometry("400x200")

# Label and input for the URL
url_label = tk.Label(root, text="Enter YouTube Channel URL:")
url_label.pack(pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Download button
download_button = tk.Button(root, text="Download All as MP3", command=start_download)
download_button.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
