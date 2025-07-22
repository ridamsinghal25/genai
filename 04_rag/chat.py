from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from openai import OpenAI

# The process of RAG is
# User Ask the query
# Embedding model generate the embedding for user query
# The query is then serach in the vector DB
# The serach results are then passed to LLM
# The LLM take the result and then provide the response

# Load environment variables
load_dotenv()


client = OpenAI()

# Vector Embedding
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

# Vector DB
vector_db = QdrantVectorStore.from_existing_collection(
    url = "http://localhost:6333",
    collection_name="learning_vectors",
    embedding=embedding_model
)


# Take user query
query = input("> ")

# Vector similarity search in DB
search_results = vector_db.similarity_search(
    query=query,
)

context = "\n\n\n".join([f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}" for result in search_results])

print("search_results", search_results)

SYSTEM_PROMPT = f"""
You are a helpful AI Assistant who answers user queries based on the available context
retrieved from a PDF file along with page_contents and page number.

For each query:  
1. First, provide a clear and concise explanation of the user’s query using ONLY the provided context
2. Then, guide the user to the relevant page number so they can explore further.

If the answer is not present in the context, politely tell the user that the information isn’t available in the document and suggest checking the referenced page for more details.

Context:
{context}
"""



chat_completion = client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": query},
    ]
)

print(f"🤖: {chat_completion.choices[0].message.content}")