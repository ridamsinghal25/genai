from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

# Load environment variables
load_dotenv()

# Load a PDF file using PyPDFLoader
file_path = Path(__file__).parent / "nodejs.pdf"

loader = PyPDFLoader(file_path)

docs = loader.load()  # Read PDF File

# # Chunking
text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=1000,
    chunk_overlap=300,
)

# Split the document into chunks
split_docs = text_splitter.split_documents(documents=docs)

# Vector Embedding Open AI
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large",
)

# Using [embedding_model] create embeddings of [split_docs] and store in DB

vector_store = QdrantVectorStore.from_documents(
    documents=split_docs,
    url="http://localhost:6333",
    collection_name="learning_vectors",
    embedding=embedding_model
)

print("indexing of documents done")
