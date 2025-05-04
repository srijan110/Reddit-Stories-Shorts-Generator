import reddit_story_scrapper
import tts
import thumbnail
from subtitles_gen import generate_subtitles
from video_gen import generate_video
from random import choice
from youtube_uploader import upload, authenticate

authenticate("files\\client_secret.json", 'files\\oauth.json')

subreddits = ["offmychest", "confession", "TrueOffMyChest", "relationships", "shortscarystories",
    "pettyrevenge", "TodayILearned","AmITheAsshole"]

subreddit = choice(subreddits)
print(subreddit)

reddit = reddit_story_scrapper.authenticate()
id, title, content, gender, url, author = reddit_story_scrapper.get_post_from_subreddit(reddit, subreddit)

tts.speak_and_save(f"{title}\n\n{content}", f"files\\audio\\{id}.mp3", gender)

thumbnail.get_thumbnail(url, id, f"files\\thumbnail\\{id}.png")

generate_subtitles(f"files\\audio\\{id}.mp3", f"files\\subtitles\\{id}.srt")

video_duration = generate_video(f"results\\{id}.mp4", "files\\font\\futur.ttf", f"files\\audio\\{id}.mp3", "files/asset/minecraft_parkour_1.mp4", f"files\\thumbnail\\{id}.png", f"files\\subtitles\\{id}.srt")

upload(f"results\\{id}.mp4", title, f"{title} - {author}", video_duration)