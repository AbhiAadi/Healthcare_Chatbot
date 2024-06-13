from logic_modules.llm_response import get_mistral_prompt
from logic_modules.llm_response import get_mistral_response
from logic_modules.chat_processing import format_chat_history

def agent(chat_history, query):
    
    if len(chat_history) == 0:
      return None

    else:
      formatted_history = format_chat_history(chat_history)

      prompt = f'''
      You are an assistant that provide answer if user query is based on previous interactions.

      Inputs:
      Chat History: {formatted_history}
      USER Query: {query}

      When a user submits a query, compare it to previous interactions stored in the chat history. 
      If the current query is similar to previous interactions query then retrieve and return the similar response from the chat history. 
      If no similar query is found, then return None. 
      Ensure that the similarity threshold for matching queries is set appropriately to avoid incorrect matches.
        '''
      response = get_mistral_prompt(prompt)
      return response
    
def process_query(query, prompt, additional_info , chat_history ):
    # Check if a similar query is in the chat history
    response = agent(chat_history, query)
    if response:
        # print("Process Query")
        return get_mistral_response(query, response , additional_info, chat_history)

    # If not similar query found,
    response = get_mistral_response(query, prompt , additional_info, chat_history)

    return response
