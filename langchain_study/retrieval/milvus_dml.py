import numpy as np
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pymilvus import MilvusClient
from FlagEmbedding import BGEM3FlagModel

from langchain_study.model_io.lc_static_class import LS


def getClient():
    return MilvusClient(url=LS.getUri())


def insert_data():

    #1.解析文件
    docu = UnstructuredWordDocumentLoader("assets/sample.docx", mode="single").load()
    text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", "。", "！", "？", "……", "，", ""], chunk_size=500,
                                              chunk_overlap=50)
    splitter_split_documents = text_splitter.split_documents(docu)
    documents_ = splitter_split_documents[0:50]

    model = BGEM3FlagModel("/langchain_study/retrieval/assets/models/bge-m3")

    #转换成向量
    all_vectors = model.encode([doc.page_content for doc in documents_], return_dense=True, return_sparse=True)

    #获取稠密和稀疏向量
    dense_vectors = all_vectors["dense_vecs"]
    sparse_vectors = all_vectors['lexical_weights']

    #insert
    insert_data_list=[]
    for doc,dense_vec,sparse_vec in zip(documents_,dense_vectors,sparse_vectors):
        if not isinstance(dense_vec, np.ndarray) or dense_vec.dtype != np.float32:
            dense_vec = np.array(dense_vec, dtype=np.float32)
        insert_data_list.append({
            "vector": dense_vec,
            "sparse_vector": sparse_vec,
            "metadata":doc.metadata,
            "text":doc.page_content
        })
    print(documents_)
    print(insert_data_list,end="========================\n")
    client = getClient()

    client.insert(
        collection_name = "demo_collection",
        data = insert_data_list
      )

def delete_data():
    client = getClient()
    client.delete(collection_name="demo_collection",filter="id in [466554365109078139,466554365109078140]")



if __name__ == "__main__":
    #insert_data()
    delete_data()

