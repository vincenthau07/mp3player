# importing packages
from pytube import YouTube, Playlist
import os

# check for destination to save file
destination = "Z:\\program\\Python\\app\\music downloader\\music"

# url input from user
while True:
    y = input("Enter the URL of the video you want to download: \n>> ")

    try:
        yt = YouTube(y)
        
        # extract only audio
        video = yt.streams.filter(only_audio=True).first()
        
        
        
        # download the file
        out_file = video.download(output_path=destination)
        
        # save the file
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        
        # result of success
        print(yt.title + " has been successfully downloaded.")

    except:
        try:
            playlist = Playlist(y)
            for video in playlist.videos:
                stream = video.streams.filter(only_audio=True).first()
                out_file = stream.download(output_path=destination)
                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp3'
                os.rename(out_file, new_file)

                print(stream.title + " has been successfully downloaded.")
        except:
            print("ERROR")