import moviepy as mov
import srt

def generate_video(background_video_path, thumbnail_path, font_path, audio_path, subtitles_path, video_path):
    subtitles_list = []
    with open(subtitles_path) as f:
        for sub in srt.parse(f.read()):
            subtitles_list.append(mov.TextClip(text=sub.content, font=font_path, font_size=32, size=(600,300), color='#ffffff', method='caption', duration=(sub.end - sub.start).total_seconds()))

    subtitles = mov.concatenate_videoclips(subtitles_list, method='compose').with_position("top")

    thumbnail_image = mov.ImageClip(thumbnail_path).with_position("center").resized(width=608).with_duration(5)
    narrator_audio = mov.AudioFileClip(audio_path)
    background_video = mov.VideoFileClip(background_video_path).subclipped(0, narrator_audio.duration)
    background_video = background_video.cropped((background_video.w - 608) // 2, 0, ((background_video.w - 608) // 2) + 608, 1080)

    full_video = mov.CompositeVideoClip([background_video, thumbnail_image, subtitles]).subclipped(0, narrator_audio.duration)
    full_video.audio = mov.CompositeAudioClip([narrator_audio])

    full_video.write_videofile(video_path, codec="libx264", audio_codec="aac", fps=20, threads=16, preset='ultrafast', ffmpeg_params=['-crf', '30'])

if __name__ == "__main__":
    generate_video("files/asset/minecraft_parkour_1.mp4", f"files\\thumbnail\\1k11fik.png", "files\\font\\futur.ttf", f"files\\audio\\1k11fik.mp3", f"files\\subtitles\\1k11fik.srt", f"results\\1k11fik.mp4")
