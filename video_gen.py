import av
import time
from PIL import Image, ImageFont, ImageDraw
import srt
import threading

mux_lock = threading.Lock()

from concurrent.futures import ThreadPoolExecutor

def wrap_text(text:str, font_size, width):
    text_list = text.split(' ')
    line = text_list[0]
    final_str = ''
    text_list.pop(0)
    
    for x in text_list:
        if len(line + ' ' + x) * font_size * 0.6 < width:
            line += ' ' + x
        else:
            final_str += '\n' + line
            line = x

    final_str += '\n' + line

    return final_str[1:]

def process_frame(frame_idx, frame, thumbnail, subtitles_image_data, video_stream, output):
    frame = frame.to_image()
    frame = frame.crop(((frame.width - 608) // 2, 0, (frame.width + 608) // 2, 1080))

    if frame_idx < 20 * 5:
        frame.paste(thumbnail, (0, 300))

    if subtitles_image_data and frame_idx > subtitles_image_data[0][1]:
        frame = Image.alpha_composite(frame.convert("RGBA"), subtitles_image_data[0][0])

    if subtitles_image_data and frame_idx > subtitles_image_data[0][2]:
        subtitles_image_data.pop(0)

    out_frames = av.VideoFrame.from_image(frame)
    with mux_lock:
        for packet in video_stream.encode(out_frames):
            output.mux(packet)

    return frame

def generate_video(output_path, font_path, audio_path, background_video_path, thumbnail_path, subtitles_path): 
    start_time = time.time()
    print(f"Starting: {time.time() - start_time}")

    narrator_audio = av.open(audio_path)
    background_video = av.open(background_video_path)

    font = ImageFont.truetype(font_path, size=28)

    frame_skip = background_video.streams.video[0].average_rate // 20

    output = av.open(output_path, 'w')
    video_stream = output.add_stream('h264', 20, options={
        "crf": '24',
        "preset": 'ultrafast',
        'tune': 'fastdecode',
        'movflags': '+faststart',
    })

    video_stream.height = 1080
    video_stream.width = 608
    video_stream.pix_fmt = 'yuv420p'

    in_audio_stream = narrator_audio.streams.audio[0]
    out_audio_stream = output.add_stream('mp3', rate=in_audio_stream.rate)

    video_frames = background_video.decode()

    thumbnail = Image.open(thumbnail_path)
    thumbnail = thumbnail.resize((608, int(thumbnail.height * (608 / thumbnail.width))))

    audio_stream = next(s for s in narrator_audio.streams if s.type == 'audio')
    video_duration = int(audio_stream.duration * audio_stream.time_base)
    print(video_duration)

    subtitles_image_data = []
    with open(subtitles_path) as f:
        for sub in srt.parse(f.read()):
            img = Image.new('RGBA', (608, 1080), (0,0,0,0))
            img_draw = ImageDraw.Draw(img)

            img_draw.multiline_text((304,700), wrap_text(sub.content, 28, 608), (255, 255, 255, 255), font, anchor='mm', align='center')

            subtitles_image_data.append([img, sub.start.total_seconds() * 20, sub.end.total_seconds() * 20])

    futures = []
    with ThreadPoolExecutor(max_workers=16) as executor:
        for j, frame in enumerate(video_frames):
            if j % frame_skip != 0: continue
            i = j // frame_skip
            if i > 20 * video_duration + 3: break

            if i % 20 == 0: print(f"{i // 20} sec: {time.time()-start_time}")

            futures.append(executor.submit(process_frame, i, frame, thumbnail, subtitles_image_data, video_stream, output))

        for future in futures:
            future.result()

        for packet in video_stream.encode():
            output.mux(packet)

    for packet in narrator_audio.demux(in_audio_stream):
        if packet.dts is None:
            continue
        packet.stream = out_audio_stream
        output.mux(packet)
    
    output.close()

    time_taken = time.time() - start_time
    print(f"Time taken: {time_taken}")
    
    return video_duration

if __name__ == "__main__":
    generate_video("results\\d6xoro.mp4", 'files\\font\\futur.ttf', 'files\\audio\\d6xoro.mp3', 'files\\asset\\minecraft_parkour_1.mp4', 'files\\thumbnail\\d6xoro.png', 'files\\subtitles\\d6xoro.srt')