import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
import pandas as pd

from ragas import evaluate
from ragas.metrics import (
    answer_relevancy,
    faithfulness,
    context_recall,
    context_precision,
)
from datasets import Dataset


# Setting Up the Environment (Replace with your API key)
os.environ["OPENAI_API_KEY"] = ""

# 1. Load the PDF Document
embeddings = OpenAIEmbeddings()  # Create an object for generating embeddings
llm = ChatOpenAI(model_name= 'gpt-3.5-turbo')              # Create an object to interact with the OpenAI API

pdf_loader = PyPDFLoader('data/policy-booklet-0923.pdf')
docs = pdf_loader.load()         # Load the questions from the PDF

prompt = ChatPromptTemplate.from_template("""
Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}""")

# 3. Split the Text into Individual Questions
text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)
print("Number of chunks created: ", len(documents))


# 4. Create Document Embeddings
vector = FAISS.from_documents(documents, embeddings)

# This line generates dense vector representations (embeddings) for each question. These embeddings capture the semantic meaning of the text and help retrieve relevant questions.

# 5. Build the Retrieval Chain
retriever = vector.as_retriever()
document_chain = create_stuff_documents_chain(llm, prompt)
retrieval_chain = create_retrieval_chain(retriever, document_chain)


dataset_df = pd.read_csv("dataset.csv")
dataset_to_evaluate = []
for i, row in dataset_df.iterrows():
    question = row['question']
    ground_truth = row['answer']
    predicted_answer = retrieval_chain.invoke({"input":question})
    new_row = row.to_dict()
    new_row['answer'] = predicted_answer["answer"]
    new_row['contexts'] = [context.page_content for context in predicted_answer["context"]]
    new_row['ground_truth'] = ground_truth
    dataset_to_evaluate.append(new_row)
    print("Question answered recieved.")
    
    
dataset_to_evaluate = pd.DataFrame(dataset_to_evaluate)
dataset_to_evaluate.to_csv("baseline_answers.csv")


eval_dataset = Dataset.from_pandas(dataset_to_evaluate)

result = evaluate(
    eval_dataset,
    metrics=[
        faithfulness,
        answer_relevancy,
    ],
)
store_result = result.to_pandas()
store_result.to_csv("report/baseline_result.csv")
print(result)

