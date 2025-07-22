from langchain_community.document_loaders import WebBaseLoader


loader_multiple_pages = WebBaseLoader([
    "https://docs.chaicode.com/youtube/chai-aur-html/introduction/",
    "https://docs.chaicode.com/youtube/chai-aur-html/emmit-crash-course/",
    "https://docs.chaicode.com/youtube/chai-aur-html/html-tags/"
])

docs = loader_multiple_pages.load()

print("docs[1]:", docs)