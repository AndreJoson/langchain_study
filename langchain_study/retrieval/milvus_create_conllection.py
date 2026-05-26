from pymilvus import MilvusClient, DataType


def create_milvus_client():
    client = MilvusClient(uri="http://localhost:19530", token="", )
    collections = client.list_collections()
    print(collections)
    return client


# 创建结构
def build_schema():
    client = create_milvus_client()
    schema = client.create_schema(
        auto_id=True,
    ).add_field(
        # 添加 id 字段，类型为整数，设置为主键
        field_name="id", datatype=DataType.INT64, is_primary=True
    ).add_field(
        # 添加 vector 字段，类型为浮点数向量，维度为 1024
        field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=1024
    ).add_field(
        # 添加 text 字段，类型为字符串，最大长度为 1500
        field_name="text", datatype=DataType.VARCHAR, max_length=1500
    ).add_field(
        field_name="metadata", datatype=DataType.JSON
    ).add_field(
        field_name="sparse_vector", datatype=DataType.SPARSE_FLOAT_VECTOR
    )
    return schema


def build_index():
    index_params = MilvusClient.prepare_index_params()
    index_params.add_index(
        field_name="vector",
        index_type="HNSW",
        metric_type="L2",
    )
    index_params.add_index(
        field_name="sparse_vector",
        index_type="SPARSE_INVERTED_INDEX",
        metric_type="IP",
    )
    return index_params


def create_collection(client):
    client.drop_collection("demo_collection")
    if not client.has_collection("demo_collection"):
        print("collection demo_collection not exists, create it")
        client.create_collection("demo_collection",
                                 schema=build_schema(),
                                 index_params=build_index())

        print(client.list_collections())

        print(client.describe_collection("demo_collection"))


create_collection(create_milvus_client())
