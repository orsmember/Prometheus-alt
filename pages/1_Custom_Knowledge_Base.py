# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 09:13:38 2023

@author: SB
"""

import streamlit as st
from streamlit_pills import pills
#from llama_index import SimpleDirectoryReader, GPTVectorStoreIndex, ServiceContext
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, ServiceContext

from pathlib import Path
import os
import openai
#from llama_index import StorageContext, load_index_from_storage
from llama_index.core import StorageContext, load_index_from_storage

openai.api_key = os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']


st.set_page_config(page_title = 'Introduction', page_icon="🧊",
                   
                   menu_items={
                       'Report a bug': "https://www.google.com",
                       'About': "# Just a demo for purpose of AI initiative!"
                                }
                   )

hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


with st.sidebar:
    st.info("""
                Use case: An AI knowledge base is a centralized information hub that can leverage generative AI capabilities to:

- Automate workflows.
- Optimize efficiency across the organization.
- Enhance onboarding and training of new colleagues.
  \n Users: Pilot project that could be extended to the whole organization.
            
            """)

 

# Create a llama session
service_context = ServiceContext.from_defaults(chunk_size_limit=256)

# Load your data to prepare data for creating embeddings
#documents = SimpleDirectoryReader(input_files=[r'C:\Users\SB\Desktop\sher.txt']).load_data()

# Embeddings are created here for your data
#global_index = GPTVectorStoreIndex.from_documents(documents)

# You can save your indexes, to be re-used again
#global_index.save_to_disk('sherlockholmes.json')

# To load vectors from local/ Allows to extract it from server also

#path = Path("Desktop\Scripts\AI\LLM\data") / "nbs.json"
path = Path("data") / "nbs.json"

storage_context = StorageContext.from_defaults(persist_dir=path)
global_index = load_index_from_storage(storage_context)

st.subheader("AI Assistant based on `Custom Knowledge Base`")

st.markdown("""
Even though LLM come with an extensive knowledge base, they may lack specific knowledge about custom cases or niche domains. This solution leverages the API of a LLM and it encorporates a specific knowledge base to create a specialized solution.
Technique used is in-context learning and the context is provided by the following public risk domain specific documents:
- Decision on Risk Management by National Bank of Serbia. 
- Law on Banks
- Decision оn the Classification of Bank Balance Sheet Assets and Off-balance Sheet Items
""")

# You can also use radio buttons instead
selected = pills("", ["OpenAI", "Huggingface"], ["🤖", "🤗"])

user_input = st.text_input("You: ",placeholder = "Ask me anything ...", key="input")

if st.button("Submit", type="primary"):
    st.markdown("----")
    res_box = st.empty()

    if selected == "OpenAI":
        query_engine = global_index.as_query_engine()
        response = query_engine.query(user_input)
        res_box.write(str(response))

    else:
        res_box.write("Work in progress!!")

st.markdown("----")
