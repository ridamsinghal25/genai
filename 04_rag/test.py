from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=1000,
    chunk_overlap=300,
)

# Load example document
with open("software_models.txt") as f:
    software_models = f.read()

text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=500,
    chunk_overlap=10,
    length_function=len,
    is_separator_regex=False,
)

split_docs = text_splitter.split_text(text=software_models)

print("split_docs[0] ",split_docs)

