from faster_whisper import WhisperModel
from datetime import timedelta
from json import load
import re

with open("files\\curseword_list.json") as f:
    curse_word_dict = load(f)
    pattern = re.compile(r'\b(' + '|'.join(re.escape(word) for word in curse_word_dict.keys()) + r')\b', re.IGNORECASE)

def remove_curse_word(text: str) -> str:
    def replacer(match):
        word = match.group(0)
        replacement = curse_word_dict.get(word.lower(), word)
        if word.isupper():
            return replacement.upper()
        elif word[0].isupper():
            return replacement.capitalize()
        else:
            return replacement
    return pattern.sub(replacer, text)


def format_timestamp(seconds: float) -> str:
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    milliseconds = int((td.total_seconds() - total_seconds) * 1000)

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60

    return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"

def write_srt(segments, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        for i, segment in enumerate(segments, start=1):
            start = format_timestamp(segment.start)
            end = format_timestamp(segment.end)
            f.write(f"{i}\n{start} --> {end}\n{remove_curse_word(segment.text.strip())}\n\n")

def generate_subtitles(audio_path, srt_path="output.srt"):
    model = WhisperModel("small", device="cpu", compute_type="int8")
    segments, _ = model.transcribe(audio_path, language="en")
    write_srt(segments, srt_path)

if __name__ == "__main__":
    generate_subtitles(f"files\\audio\\{'ugcb2i'}.mp3", f"files\\subtitles\\{'ugcb2i'}.srt")