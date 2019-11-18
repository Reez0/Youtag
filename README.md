# Youtag
 Downloads a song in .MP3 format using YoutubeDL, retrieves song details from the deezer api, and then tags the song using eyeD3. I honestly prefer "physical" music files over streaming so that's why I made this. Just pirate that shit dawg. But remember, piracy is bad mmkay?
 
 To run:
 1. `python -m venv venv`
 2. `denv\Scripts\activate`
 2. `pip install -r requirements.txt`
 3. To download and tag a single video use `python youtag.py get_video --url=<Your url here>`
 4. To download a bunch of videos use `python youtag.py get_videos --urls=<Your url 1, Your url 2...>`
 
 So far, any accented characters causes the .mp3 file to become unreadable by eyeD3 so I'll have to figure out a workaround for that at some point. When downloading a bunch of videos, make sure the delimiter is a comma, otherwise it will interpret the string as one video and blow up the planet. E.g `python youtag.py get_videos --urls="https://www.youtube.com/watch?v=dQw4w9WgXcQ, https://www.youtube.com/watch?v=2ZIpFytCSVc"`
 
 If Deezer is unable to find any information for the song, no tagging will take place, but the downloaded file will remain. That's something I guess.
 
 I will also have to add some additional conditions since youtube video urls come in multiple formats. The classic https://www.youtube.com/watch?v=dQw4w9WgXcQ, and the shortened https://youtu.be/dQw4w9WgXcQ
 
