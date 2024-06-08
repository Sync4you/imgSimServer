from .Server import connect_milvus, disconnect_milvus
from .Config import MILVUS_COLLECTION_NAME, MILVUS_DATABASE_NAME, TOP_K_IMGS, IMG_DATAPATH
from pymilvus import Collection, db


import os
import numpy as np
from PIL import Image



image_path = "/home/wuwei/workfile/test_search_images/"
search_params = {
        "metric_type": "L2",
        "offset": 5,
        "ignore_growing": False,
        "params": {"nprobe": TOP_K_IMGS}
    }
# PARTITIONS = ["ptn_" + p for p in os.listdir(data_path)]
# collection.load(partition_names=[PARTITIONS[1]])
# collection.load()


def get_connection():
    connect_milvus()
    db.using_database(MILVUS_DATABASE_NAME)
    collection = Collection(MILVUS_COLLECTION_NAME)
    return collection


def searchSim(collection, image_path, MODEL, topk=10):
    DATAS = MODEL.extractFT(image_path)
    print("extract done")
    results = collection.search(
        data=DATAS,
        anns_field="image_intro",
        # the sum of `offset` in `param` and `limit`
        # should be less than 16384.
        param=search_params,
        limit=topk,
        expr=None,
        output_fields=['image_path'],
        consistency_level="Strong"
    )
    print("milvus done")
    res = []
    for hit in results[0]:
        #print("ID: " + hit.entity.id + " distance:" + hit.distance + " path: " + hit.entity.get("image_path"))
        path = hit.entity.get("image_path")
        path = path.replace('/mnt/weeddata/imgs/', '')
        res.append({"id": hit.entity.id, "distance": hit.distance, "path": path})

    return {"output": res}



def searchSim_batch(collection, image_path, MODEL, topK=10):
    DATAS = MODEL.extractFT(image_path)

    results = collection.search(
        data=DATAS,
        anns_field="image_intro",
        # the sum of `offset` in `param` and `limit`
        # should be less than 16384.
        param=search_params,
        limit=topK,
        expr=None,
        output_fields=['image_path'],
        consistency_level="Strong"
    )

    outputs = []
    for res in results:
        lst = []
        for hit in res:
            print("ID: " + hit.entity.id + " distance:" + hit.distance + " path: " + hit.entity.get("image_path"))
            lst.append({"id": hit.entity.id, "distance": hit.distance, "path":hit.entity.get("image_path")})
        outputs.append(lst)
        print("----------------------")

    return outputs



# results[0].ids
# results[0].distances
# hit = results[0][0]
# hit.entity.get('title')
