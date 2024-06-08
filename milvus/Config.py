
IMG_DATAPATH = r"/mnt/weeddata/imgs/"

TOP_K_IMGS = 10

MILVUS_DATABASE_NAME = "imageDB"

MILVUS_USER_NAME = "root"

MILVUS_COLLECTION_NAME = "clip_images"

MILVUS_USER_PASSWORD = "Milvus"

MILVUS_HOST = "222.186.42.181"

MILVUS_PORT = "19530"

VECTOR_DIMENSION = 768

VECTOR_FIELD_NAME = "image_intro"

INDEX_PARAMS = {
  "metric_type": "L2",
  "index_type": "IVF_FLAT",
  "params": {"nlist": 1024}
}
