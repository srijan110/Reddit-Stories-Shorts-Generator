from youtube_upload.client import YoutubeUploader

def upload(video_path, secrets_file_path, title, description, video_duration):
    uploader = YoutubeUploader(secrets_file_path= secrets_file_path)
    uploader.authenticate()

    options = {
        "title": title,
        "description": description,
        "tags": ["reddit", "storytime"],
        "categoryId": "22",
        "privacyStatus": "public",
        "kids": False }

    if video_duration < 180:
        options["tags"] = ["shorts", "reddit", "storytime"]
    
    uploader.upload(video_path, options)

    uploader.close()