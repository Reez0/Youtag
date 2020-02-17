# Youtag
 Downloads a song in .MP3 format using YoutubeDL, retrieves song details from the deezer api, and then tags the song using eyeD3.
 
 To run:
 1. `python -m venv venv`
 2. `denv\Scripts\activate`
 2. `pip install -r requirements.txt`
 3. To download and tag a single video use `python youtag.py get_video --url=Your url here`
 4. To download a bunch of videos use `python youtag.py get_videos --urls=Your url 1, Your url 2...`
 
 If Deezer is unable to find any information for the song, no tagging will take place, but the downloaded file will remain.
 
