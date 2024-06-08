from pymilvus import connections, db, CollectionSchema, FieldSchema, DataType, Collection
from logging import Logger
from Config import VECTOR_DIMENSION, MILVUS_COLLECTION_NAME, MILVUS_HOST, MILVUS_PORT
from Server import connect_milvus, disconnect_milvus


connect_milvus()


if "imageDB" not in db.list_database():
    database = db.create_database("imageDB")
    print("create database imageDB newly")


db.using_database("imageDB")

image_id = FieldSchema(
    name="image_id",
    dtype=DataType.INT64,
    is_primary=True,
    auto_id=True,
    description="Key id of each image.",
)

image_path = FieldSchema(
    name="image_path",
    dtype=DataType.VARCHAR,
    max_length=255,
    default_value="nil",
    description="File path of the image.",

)

image_intro = FieldSchema(
    name="image_intro",
    dtype=DataType.FLOAT_VECTOR,
    dim=VECTOR_DIMENSION,
    description="CLIP model features vector of the image.",
)
FIELDS = [image_id, image_path, image_intro]


SCHEMA = CollectionSchema(
    fields=FIELDS,
    description="Image similarity search.",
    enable_dynamic_field=True,
)

# utility.reset_password('root', 'Milvus', 'Wuwei2023', using='default')

collection = Collection(
    name=MILVUS_COLLECTION_NAME,
    schema=SCHEMA,
    shards_num=15,
    using='default',
)

