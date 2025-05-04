from youtube_upload.client import YoutubeUploader
import json
from datetime import datetime
import os

oauth_path = ''

def authenticate(secrets_file_path, oauth_file_path):
    global oauth_path

    oauth_path = oauth_file_path
    with open(oauth_path) as f:
        doc = json.load(f)

    if datetime.strptime(doc['token_expiry'], r"%Y-%m-%dT%H:%M:%SZ") > datetime.now():
        os.remove(oauth_path)

    uploader = YoutubeUploader(secrets_file_path= secrets_file_path)
    uploader.authenticate(oauth_path)


def upload(video_path, title, description, video_duration):
    with open(oauth_path) as f:
        oauth = f.read()

    options = {
        "title": title,
        "description": description,
        "tags": ["reddit", "storytime"],
        "categoryId": "22",
        "privacyStatus": "public",
        "kids": False 
    }

    if video_duration < 180:
        options["tags"] = ["shorts", "reddit", "storytime"]
    
    uploader.upload(video_path, options)
    del(uploader)

    with open(oauth_path) as f:
        f.write(oauth)

if __name__ == "__main__":
    authenticate("files\\client_secret.json", 'files\\oauth.json')
    upload('results/e5k3z2.mp4', 'Test Video', 'Test Video', 300)