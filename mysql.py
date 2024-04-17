# %%
import os, sys
from dotenv import load_dotenv, find_dotenv

load_dotenv(sys.path[0])
# os.environ ["OPENAI_API_KEY"] = os.getenv("OPEN_API_KEY")
print(sys.path)
print (os.environ ["OPENAI_API_KEY"])
print (os.getenv("LANGCHAIN_API_KEY"))
os.environ["LANGCHAIN_TRACING_V2"] = "true"

db_user = "root"
db_password = "sql123"
db_host="127.0.0.1:3308"
db_name = "classicmodels"

from langchain_community.utilities.sql_database import SQLDatabase
db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")
# print(db.dialect)
# print(db.get_usable_table_names())
# print(db.table_info)

# %% [markdown] The above is a conenction string for mysql database
#%%
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI

llm = ChatOpenAI (model="gpt-3.5-turbo", temperature=0)
generate_qry = create_sql_query_chain(llm, db)

query = generate_qry.invoke({"question": "what is price of `1968 Ford Mustang`"})
print(query)
                              
# %%
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
execute_query = QuerySQLDataBaseTool(db=db)
execute_query.invoke(query)

# %%
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder,FewShotChatMessagePromptTemplate,PromptTemplate

examples = [
     {
         "input": "List all customers in France with a credit limit over 20,000.",
         "query": "SELECT * FROM customers WHERE country = 'France' AND creditLimit > 20000;"
     },
     {
         "input": "Get the highest payment amount made by any customer.",
         "query": "SELECT MAX(amount) FROM payments;"
     }
 ]

example_prompt = ChatPromptTemplate.from_messages(
     [
         ("human", "{input}\nSQLQuery:"),
         ("ai", "{query}"),
     ]
 )
few_shot_prompt = FewShotChatMessagePromptTemplate(
     example_prompt=example_prompt,
     examples=examples,
     input_variables=["input"]
 )

print(few_shot_prompt)

# %%
from langchain_community.vectorstores import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings

vectorstore = Chroma()
vectorstore.delete_collection()
example_selector = SemanticSimilarityExampleSelector.from_examples(
    examples,
    OpenAIEmbeddings,
    vectorstore,
    k=2,
    input_keys=["input"]
)

# %%
import pandas as pd
import numpy as np

# s = pd.Series(index=['a','b','c','d','e'])
d = {"b": 1, "a": 0, "c": 2}
s = pd.Series(d)
print (s[s > s.median()])
print (np.exp(s))