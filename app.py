from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.llms.openai import OpenAI
from langchain_experimental.sql import SQLDatabaseChain
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import HumanMessagePromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import os
import streamlit as st
import pandas as pd


#Streamlit page configuration
st.set_page_config(page_title="EzQL",layout='wide',page_icon=":bar_chart:")

# Initialising LLM
llm = ChatOpenAI(temperature=0, openai_api_key=os.getenv('openai_api_key'))

# Constructing Databse URL

host = 'localhost'
port = '3306'
username = 'root'
password = '1354267098'
database_schema = 'assetDB'
mysql_uri = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database_schema}"

db = SQLDatabase.from_uri(mysql_uri, include_tables=['plant_details', 'tag_details', 'timeseries', 'asset_details', 'kpi_assets', 'kpi_plant'],sample_rows_in_table_info=2)

db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

def retrieve_from_db(query: str) -> str:
    db_context = db_chain(query)
    db_context = db_context['result'].strip()
    return db_context


def generate(query: str) -> str:
    db_context = retrieve_from_db(query)
    
    system_message = """You are a professional representative of an On-site monitoring agency.
        You have to answer user's queries and provide relevant information from the database provided. 
        Example:
        
        Input:
        Which are the two major sites in the following data ?
        
        Context:
        The two major sites on which this data is collected are:
        1. Jhansi
        2. Hapasar
        
        Output:
        The two major sites in the following data are:
        1. Jhansi Hirpara
        """
    
    human_qry_template = HumanMessagePromptTemplate.from_template(
        """Input:
        {human_input}
        
        Context:
        {db_context}
        
        Output:
        """
    )
    messages = [
      SystemMessage(content=system_message),
      human_qry_template.format(human_input=query, db_context=db_context)
    ]
    response = llm(messages).content
    return response 

st.markdown("<h1 style='text-align: center; color: #927fe6; padding:0px 100px 20px 100px;font-size:4rem'>SQL Chatbot</h1>", unsafe_allow_html=True)
# st.markdown("<h2 style='text-align: center; color: #927fe6; padding:0px 100px 80px 100px;font-size:2rem;'>Run SQL commands and interact with your data without writing any code</h2>", unsafe_allow_html=True)

col1, col2 = st.columns([5, 2])

with col1 :
    st.header("Interact with your Data", divider="violet")
    input_text = st.text_area("Enter your query")
    if input_text is not None:
        if st.button("Enquire"):
            st.info(input_text)
            result = generate(input_text)
            if isinstance(result, pd.DataFrame):
                    st.dataframe(result)
            else:
                 st.success(result)

with col2 :
    chain_starter = st.button("Connect DB", type="secondary")
    if chain_starter:
        st.success("Database successfully connected")

# LOAD DATA INFILE '/Users/skar3krow/Desktop/LLM/langchain_sql_llm/resources/Jhansi_assets.csv'
# INTO TABLE jhansi_hirpara_assets
# FIELDS TERMINATED BY ','     
# IGNORE 1 ROWS;