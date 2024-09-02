import speech_recognition as sr
import pyaudio
import time
import wave
import torch
from faster_whisper import WhisperModel, BatchedInferencePipeline




# Function to record audio from the microphone
def record_audio():
    """
    Records audio from the microphone for a specified duration and
    writes it to a WAV file.

    Args:
        None

    Returns:
        None
    """
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 5

    # Initialize audio stream
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    # Start recording
    print("Recording...")
    frames = []
    start_time = time.time()
    while True:
        data = stream.read(CHUNK)
        frames.append(data)
        if time.time() - start_time > RECORD_SECONDS:
            break

    # Stop recording and save audio file
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save audio file
    output_file = "output.mp3"
    with wave.open(output_file, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    print("Audio saved as", output_file)
    
def transcribe():
    model_size = "large-v3"

    # Run on GPU with FP16
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    batched_model = BatchedInferencePipeline(model=model)
    segments, info = batched_model.transcribe("output.mp3", batch_size=16)

    for segment in segments:
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

# Function to transcribe the recorded audio
def transcribe_audio():
    """
    Transcribes the recorded audio using the Google Web Speech API.

    Args:
        None

    Returns:
        None
    """
    r = sr.Recognizer()

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.record(source, duration=5)
        try:
            # Use the Google Web Speech API to transcribe the audio
            text = r.recognize_google(audio)
            print("You said: " + text)
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

# Record audio and transcribe it
transcribe()
