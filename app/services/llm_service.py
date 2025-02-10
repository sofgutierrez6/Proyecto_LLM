from langchain.llms import Ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from typing import List, Dict

class LLMService:
    def __init__(self):
        self.llm = Ollama(model="llama2")
        self.embeddings = OllamaEmbeddings(model="llama2")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

    async def process_document(self, content: str) -> Dict:
        # Split the document into chunks
        texts = self.text_splitter.split_text(content)
        
        # Create vector store
        vectorstore = Chroma.from_texts(
            texts,
            self.embeddings,
            collection_name="document_collection"
        )
        
        # Create retriever
        retriever = vectorstore.as_retriever()
        
        # Create QA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever
        )
        
        # Generate summary
        summary_prompt = "Please provide a comprehensive summary of the document."
        summary = await self.llm.agenerate([summary_prompt + "\n\n" + content])
        
        return {
            "summary": summary.generations[0][0].text,
            "qa_chain": qa_chain
        }

    async def ask_question(self, qa_chain: RetrievalQA, question: str) -> str:
        response = await qa_chain.arun(question)
        return response