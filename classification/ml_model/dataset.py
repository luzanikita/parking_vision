from pathlib import Path

import numpy as np
from PIL import Image
import torch
from torchvision import transforms


def collate_fn(batch):
    batch = list(filter(lambda x: x is not None, batch))
    return torch.utils.data.dataloader.default_collate(batch)


class ParkingLotDataset:
    def __init__(self, annotation_df, trans=None):
        self.annotations = annotation_df
        if trans is not None:
            self.trans = trans
        else:
            self.trans = transforms.Compose([
                transforms.Resize(224),
                transforms.ToTensor(),
                transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
            ]) 
    
    def __getitem__(self, index):
        try:
            annotation = self.annotations.iloc[index]
            x = int(annotation["x"])
            y = int(annotation["y"])
            side = int(annotation["side"])
            img_path = annotation["img_path"]
            img = np.asarray(Image.open(img_path).convert("RGB"))
            img = img[y:y+side, x:x+side]
            img = Image.fromarray(img)
            img = self.trans(img)
            label = annotation.get("label", 0)
            return img, label
        except:
            return None
    
    def __len__(self):
        return self.annotations.shape[0]
