import streamlit as st 
# from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate,HumanMessagePromptTemplate,SystemMessagePromptTemplate


# Load environment variables from the .env file
# load_dotenv()

# Retrieve the OpenAI API key from the environment variables
openai_api_key = st.secrets['OPENAI_API_KEY']

# Validate API key (OpenAI API key not found. Make sure it's set in the .env file.)
if not openai_api_key:
    st.error("OpenAI API key not found. Make sure it's set in the .env file.")

# Initialize the OpenAI chat model
llm = ChatOpenAI(model="gpt-3.5-turbo",openai_api_key=openai_api_key)

# Define Prompt Template
# 
# 1. Define the system's role as a translator assistant.
#    You are a helpful assistant that translates text into other languages.
system_message = SystemMessagePromptTemplate.from_template(
    "You are a helpful assistant that translates text into other languages."
)

#
# 2. Define the human's input format for specifying translation details.
#    Translate the following into {language}:\n{text}
#

human_message = HumanMessagePromptTemplate.from_template(
    "Translate the following into {language}:\n{text}"
)


# 3. Combine system and human messages into a single chat prompt template.

prompt = ChatPromptTemplate.from_messages([system_message,human_message])

# Streamlit UI
st.set_page_config(page_title="Translation chatbot")
st.title("Translation language Chatbot")

# Dropdown for selecting language
language= st.selectbox("Select Language",["Urdu","English","German"])


# Text input for user text
text = st.text_input("Please enter the text to translate")

# Translate button
if st.button("Translate"):
    if not text.strip():
        st.error("Please enter the text to translate")
    else:
        
        # Generate the formatted prompt
        format_text=prompt.format_messages(language=language,text=text)
        
        # Get the response from OpenAI
        response = llm(format_text)
        
        # Extract and display the translation
        translation = response.content
        
        st.success(f"Translation text in to {language}")
        st.write(translation)
