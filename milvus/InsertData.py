from pymilvus import Collection, utility, db
from Config import MILVUS_COLLECTION_NAME
from Server import connect_milvus
import torch
import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--cate", type=str, default="13020C00")
arg = parser.parse_args()
DATA_PTH = '/home/wuwei/imgVecdata'
# CATEGORY = '13020C00'
CATEGORY = arg.cate
BATCH_SIZE = 2000


def getImgPathDict(path):
    path_dict = {}
    with open(path, "r", encoding="utf-8") as f:
        d = f.readline()
        d = f.readline()
        while d:
            d = d.replace('\n', '').split(',')
            path_dict[d[0]] = d[1]
            d = f.readline()
    return path_dict

connect_milvus()
db.using_database("imageDB")


collection = Collection(MILVUS_COLLECTION_NAME)

print(f"start reading features of images! Class  {CATEGORY}!----{datetime.datetime.now()}", flush=True)
vec_dict = torch.load(DATA_PTH + '/' + CATEGORY + '.image_vector.pth')
print(f"finish reading features of images! Class  {CATEGORY}!----{datetime.datetime.now()}", flush=True)
img_path_dict = getImgPathDict(DATA_PTH + '/' + CATEGORY + '.img_data.csv')
print(f"start inserting {CATEGORY} data to collection {MILVUS_COLLECTION_NAME}!----{datetime.datetime.now()}", flush=True)

cnt = 0
vec_data = []
img_path_data = []
all_data = []



for k, v in vec_dict.items():
    img_path = img_path_dict[str(k)]
    feature_vec = v[0].cpu().numpy().tolist()
    img_path_data.append(img_path)
    vec_data.append(feature_vec)

    cnt += 1

    if cnt % BATCH_SIZE == 0:
        all_data = [
            img_path_data,

            vec_data
        ]
        mr = collection.insert(data=all_data, partition_name=f"ptn_{CATEGORY}")
        print(f"finish inserting {cnt} piece data to collection {MILVUS_COLLECTION_NAME}!----{datetime.datetime.now()}",
              flush=True)
        vec_data = []
        img_path_data = []
        all_data = []

all_data = [
            img_path_data,

            vec_data
        ]
# mr = collection.insert(data=all_data, partition_name=f"ptn_{CATEGORY}")
mr = collection.insert(data=all_data)
print(f"finish inserting {cnt} piece data to collection {MILVUS_COLLECTION_NAME}!----{datetime.datetime.now()}",
              flush=True)
