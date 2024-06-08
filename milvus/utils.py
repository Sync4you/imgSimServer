from pymilvus import Collection, utility
from Config import MILVUS_COLLECTION_NAME, INDEX_PARAMS, VECTOR_FIELD_NAME


def show_collection():
    collection = Collection(MILVUS_COLLECTION_NAME)
    for i in collection.indexes:
        print(i)

    print(collection.partitions)

    print(collection.num_shards)

    print(collection.schema)


def drop_collection():
    utility.drop_collection(collection_name=MILVUS_COLLECTION_NAME)


def buildIndex():
    collection = Collection(MILVUS_COLLECTION_NAME)
    collection.create_index(index_params=INDEX_PARAMS, field_name=VECTOR_FIELD_NAME)
    utility.index_building_progress(MILVUS_COLLECTION_NAME)

