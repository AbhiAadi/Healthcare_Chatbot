import json
# file_path='chat_history.json'
def save_chat_history(chat_history , file_path ):
 
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(chat_history, file, ensure_ascii=False, indent=4)


def format_chat_history(chat_history):
    formatted_history = ""
    for entry in chat_history:
        role = entry['role'].capitalize()
        content = entry['content']
        formatted_history += f"{role}: {content}\n"
    return formatted_history