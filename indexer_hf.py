# from langchain_experimental.text_splitter import SemanticChunker
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Load documents from a directory
loader = DirectoryLoader("/home/abi/nfs/rafoc/plkn/", glob="**/*.txt",
                            show_progress=True)

print("dir loading ...")

documents = loader.load()

# Create embedding
print("vector embedding ...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2",
                                   model_kwargs = {'device': 'cpu'},
                                   show_progress=True)

# Create Semantic Text Splitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=300,
    add_start_index=True,
)

# Split documents into chunks
texts = text_splitter.split_documents(documents)

# Create vector store
vectorstore = Chroma.from_documents(
    documents=texts, 
    embedding=embeddings,
    persist_directory="./vector_db")

print("vectorstore created")