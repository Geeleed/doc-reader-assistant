from sentence_transformers import SentenceTransformer

embedder = SentenceTransformer('BAAI/bge-m3')
host = "localhost"
port = 8000