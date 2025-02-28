import streamlit as st 
import ollama
import requests
from chatbot import Chatbot
import duckdb
import dask.dataframe as dd
from queryProcessor import queryProcessor

chatbotObj = Chatbot()
queryProcessor = queryProcessor()
@st.cache_resource
def runSql(query):
    print("Trying to run")

    st.session_state['df'] = dd.read_csv( "s3://app1data/geoguessr-user-data-12-12-2024.csv", storage_options={"anon": False}, dtype={'suspendedUntil': 'object'}).compute()
    duckdb.register("df", st.session_state.df)

    # Compute the result (only when needed)
    print(f"Trying to run {query}")
    st.session_state['result'] = duckdb.sql(query).df()
    print("Query successful")
    return st.session_state['result']

with st.form("Query AI"):
    
    queryPlain = st.text_input(label="What do you need to do?")

    st.session_state['queryPlainSubmit'] = st.form_submit_button("Ask!")
    st.session_state['responseObj'] = chatbotObj.get_response(message=queryPlain)

    if st.session_state['queryPlainSubmit']:
        if chatbotObj.checkForSQL(message=queryPlain) == "Yes":

            st.session_state['query'] = chatbotObj.get_response(message=queryPlain)
            st.write(st.session_state['query'])

with st.form("Query Editor"):

    if 'query' in st.session_state:

        st.session_state['query'] = queryProcessor.cleanQuery(st.session_state['query'])
        st.session_state['editedQuery'] = st.text_input("Edit the query:", st.session_state['query'])
        st.session_state['queryRunButton'] = st.form_submit_button("Run SQL")
        
        if st.session_state['queryRunButton']:
            
            st.dataframe(queryProcessor.runSql(st.session_state['editedQuery']))

