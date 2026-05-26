import numpy as np
from langchain_openai import ChatOpenAI
from pymilvus import MilvusClient, AnnSearchRequest, RRFRanker
from FlagEmbedding import BGEM3FlagModel
from typing import List


def get_milvus_client():
    return MilvusClient(uri="http://localhost:19530")


def get_bge_m3_model():
    return BGEM3FlagModel("/langchain_study/retrieval/assets/models/bge-m3")


def encode_query(query: str, model: BGEM3FlagModel):
    all_embeddings = model.encode([query], return_dense=True, return_sparse=True)
    dense_vec = all_embeddings["dense_vecs"][0]
    sparse_vec = all_embeddings["lexical_weights"][0]
    print(sparse_vec)
    return dense_vec, sparse_vec


# 输出格式化
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


# 稠密向量检索
def dense_vector_search_example(client: MilvusClient, query: str, limit: int = 5):
    model = get_bge_m3_model()
    dense_vec, sparse_vec = encode_query(query, model)
    dense_vec = np.array(dense_vec, dtype=np.float32)
    result = client.search(collection_name="demo_collection", data=[dense_vec], anns_field="vector", limit=limit,
                           search_params={"metric_type": "L2"}, output_fields=["id", "text", "metadata"])
    print("稠密向量检索（vector)", result[0])
    return result


# 稀疏向量检索
def sparse_vector_search_example(client, query: str, limit: int = 5):
    model = get_bge_m3_model()
    _, sparse_vec = encode_query(query, model)
    result = client.search(collection_name="demo_collection", data=[sparse_vec], anns_field="sparse_vector",
                           limit=limit,
                           search_params={"metric_type": "IP"}, output_fields=["id", "text", "metadata"])
    print("稀疏向量检索（sparse_vector)", result[0])
    return result

#混合检索
def hybrid_vector_search_example_rrf(client:MilvusClient, query: str, limit: int = 5):
    model = get_bge_m3_model()
    dense_vec, sparse_vec = encode_query(query, model)
    dense_vec = np.array(dense_vec, dtype=np.float32)
    dense_req = AnnSearchRequest(data=[dense_vec], anns_field="vector", param={"metric_type": "L2"}, limit=limit)
    sparse_req = AnnSearchRequest(data=[sparse_vec], anns_field="sparse_vector", param={"metric_type": "IP"}, limit=limit)
    results = client.hybrid_search(collection_name="demo_collection", reqs=[dense_req, sparse_req],
                                  ranker=RRFRanker(k=60), limit=limit, output_fields=["id", "text", "metadata"])
    print("混合检索",results[0])
    return results

#rag数据库返回结果交给llm处理
def rag_demo(client:MilvusClient,query):
    llm = ChatOpenAI(model="gpt-4o-mini")
    retrieval_res = hybrid_vector_search_example_rrf(client=client, query=query)
    print(retrieval_res)
    context = "\n".join(data[0].entity.text for data in retrieval_res)
    message


if __name__ == "__main__":
    # encode_query("中国宪法讲了啥",get_bge_m3_model())
    # dense_vector_search_example(get_milvus_client(),"讲讲合同法律问题")
    #sparse_vector_search_example(get_milvus_client(), "讲讲合同法律问题")
    #hybrid_vector_search_example_rrf(get_milvus_client(),"讲讲合同法律问题")
    rag_demo(get_milvus_client(),"不动产被占有了怎么办？")
