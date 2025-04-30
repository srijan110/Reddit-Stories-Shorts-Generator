from youtube_upload.client import YoutubeUploader

def upload(video_path, secrets_file_path, title, description):
    uploader = YoutubeUploader(secrets_file_path= secrets_file_path)
    uploader.authenticate()

    
    options = {
        "title": title,
        "description": description,
        "tags": ["shorts", "reddit", "funny", "storytime"],
        "categoryId": "22",
        "privacyStatus": "public",
        "kids": False } 
    

    #video_path = "results/1ka42re.mp4"
    uploader.upload(video_path, options)

    uploader.close()