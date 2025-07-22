from langchain_community.document_loaders import WebBaseLoader


loader_multiple_pages = WebBaseLoader([
    "https://github.com/ridamsinghal25/genai"
])

docs = loader_multiple_pages.load()

print("docs[1]:", docs)