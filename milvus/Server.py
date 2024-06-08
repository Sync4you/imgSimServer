from pymilvus import connections
from .Config import MILVUS_USER_NAME, MILVUS_USER_PASSWORD, MILVUS_HOST, MILVUS_PORT

ALIAS_CON = "default"


def connect_milvus():
    connections.connect(
            alias=ALIAS_CON,
            user=MILVUS_USER_NAME,
            password=MILVUS_USER_PASSWORD,
            host=MILVUS_HOST,
            port=MILVUS_PORT
        )
    print(f"Connected to {MILVUS_HOST}")


def disconnect_milvus():
    connections.disconnect(ALIAS_CON)
    print(f"Disconnected from {MILVUS_HOST}")

