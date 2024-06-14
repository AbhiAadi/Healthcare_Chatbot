import chainlit as cl
from logic_modules.extract_text import process_file
from logic_modules.chromadb_upload import chromadb_load
import asyncio

persist_directory = "Data/Chromadata"

@cl.on_chat_start
async def on_chat_start():
    # Sending a welcome message
    await cl.Message(content="Hello, this is your secure Medical Clinic Note Generation Bot!").send()
    
    pdf_file = None
    # Wait for the user to upload a PDF file
    while pdf_file == None:
        pdf_file = await cl.AskFileMessage(
            content="Please upload the PDF file which contains the additional information!",
            accept=["application/pdf"],
            max_size_mb=20,
        ).send()

    pdf = pdf_file[0]
    await cl.Message(content="Processing the PDF file, this may take a moment...").send()

    # Run the processing and vectorization in a background task
    print(pdf.path)
    #pdf_text = await asyncio.to_thread(process_file, pdf.path, pdf.name)
    #await asyncio.to_thread(chromadb_load, pdf_text, persist_directory)
    pdf_text = process_file(pdf.path, pdf.name)
    chromadb_load(pdf_text, persist_directory)
    
    await cl.Message(content=f"`{pdf.name}` uploaded and processed successfully!").send()


