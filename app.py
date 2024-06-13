import chainlit as cl
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
from logic_modules.agent import process_query
from logic_modules import chat_processing
from logic_modules.extract_text import process_file
from logic_modules.chromadb_extract import chromadb_retreive
from io import BytesIO
import asyncio
import time
import datetime 
import os
persist_directory = "Data/Chromadata"
chat_history = []
# Generate a unique file path for each session
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
directory = "chat_history"
os.makedirs(directory, exist_ok=True)
file_path = os.path.join(directory, f"chat_history_{timestamp}.json")

recognizer = sr.Recognizer()

@cl.on_chat_start
async def on_chat_start():
    # Sending a welcome message
    await cl.Message(content="Hello, this is your secure Medical Clinic Note Generation Bot!").send()
    
    prompt_file = None
    # Wait for the user to upload a prompt file
    while prompt_file == None:
        prompt_file = await cl.AskFileMessage(
            content="Please upload the prompt template!" ,
            accept=["text/plain", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"],
            max_size_mb=5,
        ).send()

    prompt = prompt_file[0]
    prompt_text = process_file(prompt.path, prompt.name)
    await cl.Message(
        content=f"`{prompt.name}` uploaded successfully!"
    ).send()
    cl.user_session.set("prompt_text", prompt_text)

@cl.on_audio_chunk
async def on_audio_chunk(chunk: cl.AudioChunk):
    if chunk.isStart:
        buffer = BytesIO()
        buffer.name = f"input_audio.{chunk.mimeType.split('/')[1]}"
        cl.user_session.set("audio_buffer", buffer)
        cl.user_session.set("audio_mime_type", chunk.mimeType)
    
    cl.user_session.get("audio_buffer").write(chunk.data)

@cl.on_audio_end
async def on_audio_end():
    audio_buffer: BytesIO = cl.user_session.get("audio_buffer")
    audio_buffer.seek(0)

    try:
        # Save audio buffer to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
            temp_audio_file.write(audio_buffer.read())
            temp_audio_file_path = temp_audio_file.name

        # Convert audio file to WAV format using pydub
        audio = AudioSegment.from_file(temp_audio_file_path)
        temp_wav_path = temp_audio_file_path.replace(".mp3", ".wav")
        audio.export(temp_wav_path, format="wav")

        # Use speech_recognition to process the WAV audio
        with sr.AudioFile(temp_wav_path) as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Processing audio...")
            audio_data = recognizer.record(source)

        text = recognizer.recognize_google(audio_data)
        text = text.lower()
        cl.user_session.set("transcribed_text", text)
        await cl.Message(content=f"Transcribed text: {text}").send()

    except sr.UnknownValueError:
        await cl.Message(content="Could not understand audio").send()

    except sr.RequestError as e:
        await cl.Message(content=f"Could not request results; {e}").send()

    finally:
        # Clean up temporary files
        if temp_audio_file_path:
            try:
                os.remove(temp_audio_file_path)
                os.remove(temp_wav_path)
            except Exception as e:
                print(f"Error removing temporary files: {e}")


@cl.on_message
async def on_message(msg: cl.Message):
    
    prompt_text = cl.user_session.get("prompt_text")
    transcribed_text = cl.user_session.get("transcribed_text", None)
    
    if transcribed_text:
        user_query = transcribed_text
        cl.user_session.set("transcribed_text", None)  # Clear audio text after use
    else:
        user_query = msg.content
    # combined_query = f"{prompt_text}\n{user_query}"
    retrieved_info = chromadb_retreive(user_query, persist_directory)
    
    response = await cl.make_async(process_query)(user_query, prompt_text, retrieved_info, chat_history)

    chat_processing.save_chat_history(chat_history , file_path)
    await cl.Message(content=f"```\n{response}\n```").send()
    # await cl.Message(content=response).send()




