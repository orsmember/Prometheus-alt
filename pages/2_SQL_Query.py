# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 09:14:09 2023

@author: SB
"""
import streamlit as st
from pathlib import Path
import openai
import os
from sqlalchemy import (
    create_engine,
    MetaData,
    insert,
    Table,
    Column,
    String,
    Integer,
    Float,
    select,
    column,
    DateTime,
    ForeignKey,
    Date
)
engine = create_engine("sqlite:///:memory:")
metadata_obj = MetaData()
# create SQL tables
table_name = "accounts"
accounts = Table(
    table_name,
    metadata_obj,
    Column("customer_id", Integer, primary_key=True),
    Column("customer_name", String(10)),
    Column("customer_email", String(10)),
    Column("address", String(15)),
    Column("total_customer_balance", Float)
)

table_name = "additional"
additional = Table(
    table_name,
    metadata_obj,
    Column("accountid", Integer, primary_key=True),
    Column("customer", Integer, ForeignKey("accounts.customer_id")),
    Column("date_opened", DateTime),
    Column("interest_rate", Float),
    Column("balance", Float),
    Column("last_transaction_date", DateTime),
    Column("transaction_amount", Float)
)
metadata_obj.create_all(engine)


openai.api_key = os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']

with st.sidebar:
    st.info("""
                Use case: Querying assistant. 
- Intruduces simple querying    \n capabilities to all.
- Provides coding assistance   \n to more experiences colleagues   
- Code debuging for advanced   \n analytics, development and validation teams.
  \n Users: Analytics teams in Risk. Can be scaled to other sectors.
            
            """)


from llama_index.core import SQLDatabase, ServiceContext
from llama_index.llms.openai import OpenAI
llm = OpenAI(temperature=0, model="text-davinci-002")
service_context = ServiceContext.from_defaults(llm=llm)
sql_database = SQLDatabase(engine, include_tables=["accounts"])

#sql_database = SQLDatabase(engine, include_tables=["accounts"])

import pandas as pd


#path = Path("Desktop\Scripts\AI\LLM\data") / "mock_data.csv"
#path2 = Path("Desktop\Scripts\AI\LLM\data") / "mock_data2.csv"

path = Path("data") / "mock_data.csv"
path2 = Path("data") / "mock_data2.csv"


df = pd.read_csv(path)
df2 = pd.read_csv(path2)

df2['date_opened'] = pd.to_datetime(df2['date_opened'])
df2['last_transaction_date'] = pd.to_datetime(df2['last_transaction_date'])


for index, row in df.iterrows():
    row = {'customer_id':row['customer_id'],'customer_name': row['customer_name'], 'customer_email': row['customer_email']
           ,'address': row['address'] 
            ,'total_customer_balance': row['total_customer_balance']
          }
    stmt = insert(accounts).values(**row)
    with engine.connect() as connection:
        cursor = connection.execute(stmt)
        connection.commit()
        

for index, row in df2.iterrows():
    row = {'accountid':row['accountid'], 'customer': row['customer'],'date_opened': row['date_opened'], 'interest_rate': row['interest_rate']
           ,'last_transaction_date': row['last_transaction_date'] 
            ,'transaction_amount': row['transaction_amount']
          }
    stmt = insert(additional).values(**row)
    with engine.connect() as connection:
        cursor = connection.execute(stmt)
        connection.commit()

st.subheader("AI Assistant `SQL Queries in plan English`")



from llama_index.core import SQLDatabase, VectorStoreIndex
from llama_index.core.indices.struct_store.sql import SQLStructStoreIndex
from llama_index.core.indices.struct_store import SQLContextContainerBuilder

# build a vector index from the table schema information
context_builder = SQLContextContainerBuilder(sql_database)
table_schema_index = context_builder.derive_index_from_context(
    VectorStoreIndex,
)
# NOTE: not ingesting any unstructured documents atm
index = SQLStructStoreIndex.from_documents(
    [],
    sql_database=sql_database, 
    table_name="accounts",
)



st.markdown(
"""
Text-to-SQL is a specific natural language processing (NLP) technique where the goal is to generate SQL queries from natural language text automatically. This task is based on converting the text input into a structured representation and this representation is used to generate a semantically correct SQL query that can be executed on a database. 

  \n

By default, the text-to-SQL prompts take into account the table schema information only into the prompt. However, this can be further augmented by providing additional table context as well. This can be provided manually or derived from unstructured documents.

  \n

For the demonstration of specific use case, the following tables have been created, populated with dummy data. 
"""
    
)

col1, col2 = st.columns(2)
with col1:
    
    st.markdown(
    """
    Clients table:
    - customer_id (Primary Key)
    - customer_name
    - customer_email
    - address
    - total_customer_balance
    """
    )

with col2:  
    st.markdown(
    """
    Accounts table:
    - accountid (Primary Key)
    - customer (Foreign Key)
    - date_opened
    - interest_rate
    - last_transaction_date
    - transaction_amount
    """
    )
       

st.text('  \n  \n  \n  \n')
st.subheader('Enter a prompt to query tables above:')
user_input = st.text_input("Your prompt: ",placeholder = "Ask me anything ... e.g., Which account has the highest balance?", key="input")


context_builder.query_index_for_context(table_schema_index, user_input, store_context_str=True)
context_container = context_builder.build_context_container()


if st.button("Submit", type="primary"):
    st.markdown("----")
    res_box = st.empty()

    query_engine = index.as_query_engine(
    sql_context_container=context_container
)
    
    response = query_engine.query(user_input)
    res_box.write(str(response))
    
    
    
    res_box2 = st.empty()
    
    res_box2.write(response.metadata['sql_query'].replace('\n', '  \n'))


        
