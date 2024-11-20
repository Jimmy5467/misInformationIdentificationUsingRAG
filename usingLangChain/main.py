import os
import streamlit as st
import time
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env (especially openai api key)

def get_openai_embeddings():
    return OpenAIEmbeddings(model="text-embedding-3-large")

st.title("Fact Verifier")
st.sidebar.title("verifing sites:")

urls = []
for i in range(3):
    url = st.sidebar.text_input(f"URL {i+1}")
    urls.append(url)

process_url_clicked = st.sidebar.button("Process URLs")
file_path = "faiss_index"
main_placeholder = st.empty()
llm = OpenAI(temperature=0.9, max_tokens=500)

if process_url_clicked:
    # load data
    loader = UnstructuredURLLoader(urls=urls)
    main_placeholder.text("Data Loading...Started...✅✅✅")
    data = loader.load()
    
    # split data
    text_splitter = RecursiveCharacterTextSplitter(
        separators=['\n\n', '\n', '.', ','],
        chunk_size=1000
    )
    main_placeholder.text("Text Splitter...Started...✅✅✅")
    docs = text_splitter.split_documents(data)
    
    # create embeddings and save it to FAISS index
    embeddings = get_openai_embeddings()
    vectorstore_openai = FAISS.from_documents(docs, embeddings)
    main_placeholder.text("Embedding Vector Started Building...✅✅✅")
    time.sleep(2)
    
    # Save the FAISS index
    vectorstore_openai.save_local(file_path)
    
    main_placeholder.text("Index saved successfully! ✅✅✅")

query = main_placeholder.text_input("Post which need to get verified: ")
if query:
    if os.path.exists(file_path):
        embeddings = get_openai_embeddings()
        vectorstore = FAISS.load_local(file_path, embeddings, allow_dangerous_deserialization=True)

        # Create a custom prompt template
        template = """Use the following pieces of context to check that give social media post is factually correct or not.
        Cleary tell that given social mdeia post is that post fact correct according to cotext or not, along with reason.
        Use three sentences maximum and keep the answer as concise as possible. 
        {context}
        Question: {question}
        Helpful Answer:"""

        QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

        # Create the RetrievalQA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(),
            return_source_documents=True,
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
        )

        result = qa_chain.invoke({"query": query})
        
        st.header("Answer")
        st.write(result["result"])
        
        # Display sources, if available
        if result["source_documents"]:
            st.subheader("Sources:")
            for doc in result["source_documents"]:
                st.write(doc.metadata.get("source", "Unknown source"))

    else:
        st.error("Index files not found. Please process the URLs first.")