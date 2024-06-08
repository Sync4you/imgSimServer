import torch
import clip
from PIL import Image
import os
import threading


class ClipModel:
    def __init__(self):

        self.device = torch.device('cuda' if torch.cuda.is_available() else "cpu")
        self.model, self.preprocess = clip.load("ViT-L/14", device=self.device)
        self.model_format = "package"
        self.model_version = "L-14"
        self.lock = threading.Lock()

    def extractFT(self, img_paths):
        datas = []
        with self.lock:
            model, preprocess = self.model, self.preprocess
            # model, preprocess =  clip.load("ViT-L/14", device=device)
            image = preprocess(Image.open(img_paths)).unsqueeze(0).to(self.device)
            fts = model.encode_image(image)
            fts = fts[0].cpu().detach().numpy().tolist()
        datas.append(fts)
        print("finished loading and extracting images!")
        return datas

    def extractFT_Batch(self, img_paths):
        datas = []
        model, preprocess = self.model, self.preprocess
        # model, preprocess =  clip.load("ViT-L/14", device=device)
        for img_path in os.listdir(img_paths):
            img_path = img_paths + img_path
            image = preprocess(Image.open(img_path)).unsqueeze(0).to(self.device)
            fts = model.encode_image(image)
            fts = fts.cpu().detach().numpy().tolist()
            datas.append(fts)
        print("finished loading images!")
        return datas
