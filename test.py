from audioplayer import AudioPlayer
audiofile = AudioPlayer("music/2 chi.mp3")
audiofile.volume = 50
audiofile.play(block=True)