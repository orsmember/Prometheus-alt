# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import streamlit as st
import openai
import os

openai.api_key = os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']

with st.sidebar:
    "[![View GitHub source code](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

st.write("# Welcome to demo site on LLM Use Cases! 👋")


st.markdown(
    """
    This is a short demonstration on a few use cases related to AI LLM application that the Group 4 has identified.  \n
    **👈 You can select a demo from the sidebar** to see some the following examples
    of what AI can do!
    
    ### Custom Knowledge Base?
    In this demo, we leverage Generative AI with LLMs and external document(s) to provide custom responses to user prompts. The documents used for this demo are risk specific regulation. Solution can be scaled to additional risk documents or domains.
   
    ### SQL Queries in plain English?
    This demo explores the possibility of using the ChatGPT for providing insights using plain English. Beside empowering all to easily get responses on simple queries, it provided training opportunities and could be used for code generation, error detection and debugging for more experienced users.
"""
)



st.subheader("AI Assistant based based on GPT 3.5")



st.title("💬 Chatbot") 

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg.content)
