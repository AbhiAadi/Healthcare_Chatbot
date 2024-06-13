from langchain_community.llms import HuggingFaceEndpoint
from dotenv import load_dotenv
load_dotenv()
import os

## For running the code using Hugging Face api

REPO_ID=os.getenv('REPO_ID')
API_KEY=os.getenv("API_KEY")

def get_mistral_response(query, prompt, additional_info, chat_history):
    
    llm = HuggingFaceEndpoint(
        repo_id=REPO_ID,
        top_k=1,
        top_p=0.9,
        temperature=0.4,
        huggingfacehub_api_token= API_KEY,
    )

    # Define the prompt template
    template = f"""
    [INST]Do not respond in markdown, raw code, or any other format. Only use plain text for the response in a well structured way.
    Given the additional information and a query, critically analyze the information provided and precisely answer the query according to given prompt{prompt} strictly, without making up any false answer. If the answer is not provided in the additional information, then just say that the query can't be answered.
    Do not give reference to any response during the conversation.
    Given additional information : {additional_info}
    Given Query: {query}
    [/INST]
    """
    # template = f"""
    # [INST]
    # Follow these instructions strictly:
    # Format: Do not respond in markdown, raw code, or any other format. Only use plain text for the response in a well structured manner.
    # Critical Analysis: Given the additional information and a query, critically analyze the information provided and precisely answer the query according to given prompt strictly, without making up any false answer.
    # Accuracy: Ensure all answers are accurate and based strictly on the additional information provided. Do not fabricate or infer any information beyond what is given.
    # Response Criteria: 
    # - If the answer is explicitly stated in the additional information, provide a clear and precise answer.
    # - If the answer is not found in the additional information, explicitly state that the query cannot be answered based on the provided information.
    # - Do not add any external information, references, or context outside the provided additional information. Do not give reference for any response within the additional information provided.
    # Conciseness: Keep the response concise and to the point.
    # Structure: Ensure the response is well-structured, organized, and directly relevant to the query.
    # Relevance: Ensure that the response is directly relevant to the query and does not include unrelated information.

    # Additional Information: {additional_info}

    # Given Query: {query}

    # Prompt: {prompt}
    # [/INST]"""

    print("Generating Response...")
    response = llm.generate([template])
    chat_history.append({'role': 'user' , 'content': query})
    chat_history.append({'role': 'assistant', 'content': response.generations[0][0].text})

    return response.generations[0][0].text

def get_mistral_prompt(prompt):

    llm = HuggingFaceEndpoint(
        repo_id=REPO_ID,
        top_k=1,
        top_p=0.9,
        temperature=0.4,
        huggingfacehub_api_token= API_KEY,
    )

    template = f"""
    [INST] 
    'Return the response strictly as instructed in the prompt.  .'
    Given prompt: {prompt}
    [/INST]
    """
    response = llm.generate([template])
    response_content = response.generations[0][0].text
    return response_content



## For running the llm through ollama ......
## Uncomment the code below

# import ollama

# def get_mistral_response(query, prompt, additional_info, chat_history):
#     template = f"""
#     [INST]Follow this instruction strictly.Do not give response in markdown format or any other format like raw code, provide answer in only one format.
#     Given the additional information and a query, critically analyze the information provided and precisely answer the query according to given prompt{prompt} strictly, without making up any false answer. If the answer is not provided in the additional information, then just say that the query can't be answered.
#     Do not give reference to any response during the conversation.
#     Given additional information : {additional_info}
#     Given Query: {query}
#     [/INST]
#     """
#     print("Generating Response...")
#     response = ollama.chat(model='mistral', messages=[
#     {
#         'role': 'user',
#         'content': template,
#     },
#     ])
#     chat_history.append({'role': 'user' , 'content': query})
#     chat_history.append({'role': 'assistant', 'content': response['message']['content']})

#     responses = response['message']['content']
#     return responses

# def get_mistral_prompt(prompt):
    
#     template = f"""
#     [INST] 
#     'Return the response strictly as instructed in the prompt.  .'
#     Given prompt: {prompt}
#     [/INST]
#     """
#     response = ollama.chat(model='mistral', messages=[
#     {
#         'role': 'user',
#         'content': template,
#     },
#     ])

#     response_content = response['message']['content']
#     return response_content