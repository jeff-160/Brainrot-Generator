import pyttsx3, stable_whisper
from moviepy import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip
import os, json

audio_file = "audio.mp3"

def sanitise(word: str):
    word = word.strip()

    for i in reversed(range(len(word))):
        if word[i].isalpha() or word[i].isnumeric():
            break

    return word[0 : i + 1]

def transcribe(text: str) -> dict:
    engine = pyttsx3.init()
    engine.save_to_file(text, audio_file)
    engine.runAndWait()

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

def create_video(text, video_file, output_video):
    words = transcribe(text)

    video = VideoFileClip(video_file)
    audio = AudioFileClip(audio_file)
     
    # video = video.loop(duration=audio.duration) if audio.duration > video.duration else 
    video = video.subclipped(0, audio.duration)
    
    word_clips = []
    
    start_time = 0
    duration = 0.3
    
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
        start_time += duration
    
    video = video.with_audio(audio)
    
    composite = CompositeVideoClip([video, *word_clips])
    
    composite.write_videofile(output_video, codec="libx264", audio_codec="aac")

    os.remove(audio_file)


if __name__ == "__main__":
    with open("test.txt", "r") as f:
        text = f.read()

    create_video(text, "background.mp4", "output.mp4")