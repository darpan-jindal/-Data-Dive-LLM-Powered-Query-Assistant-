from langchain.llms import GooglePalm
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from fewshots import few_shots
from langchain.prompts import FewShotPromptTemplate
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _mysql_prompt
from langchain.prompts.prompt import PromptTemplate
import os
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
import pandas as pd
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
# from annoy import Annoy
import streamlit as st
import pandas as pd
import os

# ... other imports for GooglePalm, SQLDatabase, etc. (assuming you have them)

def getinfo():
    llm=GooglePalm(google_api_key=os.environ["key"],temperature=0.2)
    db_user = 'root'
    db_pass = 'fuk1234'
    db_host = 'localhost'
    db_name = 'atliq_tshirts'
    db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}", sample_rows_in_table_info=3)
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    texts = ["".join(example.values()) for example in few_shots]
    vector_store = FAISS.from_texts(texts=texts, embedding=embeddings, metadatas=few_shots)
    example_prompt = PromptTemplate(
        input_variables=["Question", "SQLQuery", "SQLResult","Answer",],
        template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}",
    )
    mysql_prompt = """You are a MySQL expert. Given an input question, first create a syntactically correct MySQL query to run, then look at the results of the query and return the answer to the input question.
    Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per MySQL. You can order the results to return the most informative data in the database.
    Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.
    Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
    Pay attention to use CURDATE() function to get the current date, if the question involves "today".

    Use the following format:

    Question: Question here
    SQLQuery: Query to run with no pre-amble
    SQLResult: Result of the SQLQuery
    Answer: Final answer here

    No pre-amble.
    """
    es=SemanticSimilarityExampleSelector(
        vectorstore=vector_store,
        k=2
    )
    few_shot_prompt = FewShotPromptTemplate(
        example_selector=es,
        example_prompt=example_prompt,
        prefix=mysql_prompt,
        suffix=PROMPT_SUFFIX,
        input_variables=["input", "table_info", "top_k"],
    )
    chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, prompt=few_shot_prompt)

    def get_query_and_result(input, table_info, top_k=5):
        result = chain(input, table_info, top_k)
        sql_query = result['SQLQuery']
        sql_result = result['SQLResult']
        answer = result['Answer']

        df = pd.DataFrame(sql_result)

        return {"SQLQuery": sql_query, "SQLResult": df, "Answer": answer}

    chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, prompt=few_shot_prompt)

    def get_query_and_result(input, table_info, top_k=5):
        result = chain(input, table_info, top_k)
        return result

    return get_query_and_result  # Return the function itself

get_query_and_result = getinfo()  # Call getinfo() to get the function

st.set_page_config(layout="wide", page_title="AtliQ T Shirts: Database Q&A ", page_icon="")

# ... rest of your code for styling and sidebar ...
# t.set_page_config(layout="wide", page_title="AtliQ T Shirts: Database Q&A 👕", page_icon="👕")

st.markdown("""
    <style>
    body {
        color: #fff;
        background-color: #4F8BF9;
    }
    </style>
    """, unsafe_allow_html=True)

sidebar = st.sidebar
sidebar.image("trial.jpeg")
sidebar.title("AtliQ T Shirts: Database Q&A 👕")

question = sidebar.text_input("Question: ")
# question = sidebar.text_input("Question: ")

if question:
    result = get_query_and_result(question)  # Call the function to get results

    st.header("SQL Query")
    if "SQLQuery" in result:
        st.code(result["SQLQuery"])
    else:
        st.write("No SQL Query Found")

    st.header("SQL Result")
    if "SQLResult" in result and isinstance(result["SQLResult"], pd.DataFrame):
        st.dataframe(result["SQLResult"])
    else:
        st.write("No SQL Result Found or SQL Result is not a DataFrame")

    st.header("Answer")
    if "Answer" in result:
        st.write(result["Answer"])
    else:
        st.write("No Answer Found")
