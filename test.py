from pytube import*

url="https://www.youtube.com/watch?v=qu66_oYJDNs&list=RDmrFvRJCNlwU&index=2"
yt=YouTube(url)
video_file=yt.streams.filter(progressive=True).first()
audio_file=yt.streams.filter(only_audio=True).first()
title=yt.title
thumbnail=yt.thumbnail_url
desc=yt.description[:200]

# print(thumbnail,desc)
# print(video_file)
# print(audio_file)
# video_file.download()
