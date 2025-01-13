import sys
sys.dont_write_bytecode = True

import pyttsx3, stable_whisper
from moviepy import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip, vfx
import os
from tts import tts


audio_file = "audio.mp3"

def sanitise(word: str):
    word = word.strip()

    for i in reversed(range(len(word))):
        if word[i].isalpha() or word[i].isnumeric():
            break
        
        word = word[0 : i]

    return word

def transcribe(text: str) -> dict:
    tts(text, audio_file)

    model = stable_whisper.load_model('base')
    result = model.align(audio_file, text, language='en')

    mappings = []

    for segment in result.segments:
        for word in segment.words:
            mappings.append({
                "word": sanitise(word.word),
                "start": word.start,
                "end": word.end
            })

    return mappings

def create_video(text: str, video_file: str, output_video: str):
    words = transcribe(text)

    video = VideoFileClip(video_file)
    audio = AudioFileClip(audio_file)
     
    video = video.with_effects([vfx.Loop(duration=audio.duration)]) if audio.duration > video.duration else video.subclipped(0, audio.duration)
    
    word_clips = []
    
    for word in words:
        word_clip = TextClip(
            font="font.ttf",
            text=word["word"],
            font_size=50,
            color='white',
            stroke_color="black",
            stroke_width=10,
            method="caption",
            size=(video.w, video.h)
        ).with_position("center").with_start(word["start"]).with_duration(word["end"] - word["start"]).resized(lambda t: min(0.5 + 10 * t, 1))
        
        word_clips.append(word_clip)
    
    video = video.with_audio(audio)
    
    composite = CompositeVideoClip([video, *word_clips])
    
    composite.write_videofile(output_video, codec="libx264", audio_codec="aac")

    os.remove(audio_file)


if __name__ == "__main__":
    with open("test.txt", mode="r", encoding="utf-8") as f:
        text = " ".join([word for word in f.read().split(" ") if len(sanitise(word))])

    create_video(text, "background.mp4", "output.mp4")