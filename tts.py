import asyncio
import edge_tts

def speak_and_save(text, filename="output.mp3", gender="female"):
    if gender == 'female':
        voice = "en-US-AriaNeural"
    else:
        voice = "en-US-GuyNeural"

    async def run():
        communicate = edge_tts.Communicate(text=text, voice=voice, rate="+20%")
        await communicate.save(filename)

    asyncio.run(run())

if __name__ == "__main__":
    speak_and_save("This is a natural voice from Microsoft.")