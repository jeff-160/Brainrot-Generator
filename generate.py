import stable_whisper
from moviepy import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip, vfx
import re, os, random
from tts import tts

audio_file = "audio.mp3"

def sanitise(word: str) -> str:
    return re.sub(r'^\W+|\W+$', '', word.strip())

def transcribe(text: str) -> dict:
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

def create_video(text: str, output_file: str):
    tts(text, audio_file)

    words = transcribe(text)

    video = VideoFileClip(f"assets/background/{random.choice(os.listdir('assets/background'))}")
    audio = AudioFileClip(audio_file)
     
    if audio.duration > video.duration:
        video = video.with_effects([vfx.Loop(duration=audio.duration)])
    else:
        start_time = random.uniform(0, video.duration - audio.duration)
        video = video.subclipped(start_time, start_time + audio.duration)
    
    word_clips = []
    
    for word in words:
        word_clip = TextClip(
            font="assets/font.ttf",
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
    
    composite.write_videofile(output_file, codec="libx264", audio_codec="aac")

    os.remove(audio_file)