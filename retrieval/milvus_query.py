from ast import List, Tuple, Dict

from pymilvus import MilvusClient
from FlagEmbedding import BGEM3FlagModel


def get_milvus_client():
    return MilvusClient(uri = "http://localhost:19530")

def get_bge_m3_model():
    return BGEM3FlagModel("/Users/wangbowei/PycharmProjects/langchain_study/retrieval/assets/models/bge-m3")

def encode_query(query:str,model:BGEM3FlagModel):
    all_embeddings = model.encode([query], return_dense=True, return_sparse=True)
    dense_vec = all_embeddings["dense_vecs"][0]
    sparse_vec = all_embeddings["lexical_weights"][0]
    print(sparse_vec)
    return dense_vec, sparse_vec


#输出格式化
def print_hits(title: str, hits: List[dict]):
    print("\n" + "=" * 20)
    print(title)
    print("=" * 20)
    for i, hit in enumerate(hits, start=1):
      entity = hit.get("entity", {})
      print(
        {
          "rank": i,
          "id": entity.get("id"),
          "distance": hit.get("distance"),
          "text": entity.get("text"),
          "metadata": entity.get("metadata"),
        }
      )

if __name__ == "__main__":
    encode_query("中国宪法讲了啥",get_bge_m3_model())