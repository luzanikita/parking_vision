from pathlib import Path

from typing import List, Optional
from pydantic import BaseModel
import torch
import pandas as pd
import pytorch_lightning as pl
from torch.utils.data import DataLoader

from ml_model.models import mAlexNet
from ml_model.classifier import ParkingLotClassifier
from ml_model.dataset import ParkingLotDataset, collate_fn


class Lot(BaseModel):
    id: int
    x: int
    y: int
    side: int
    is_free: Optional[bool] = True


class CameraShot(BaseModel):
    id: Optional[int] = 0
    is_available: Optional[bool] = True
    img_path: str
    lots: List[Lot]


def prepare_model(weights_path):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = mAlexNet()
    classifier = ParkingLotClassifier(model)
    classifier.model.load_state_dict(torch.load(weights_path, map_location=torch.device(device)))
    trainer = pl.Trainer()
    
    return classifier, trainer


def prepare_data(camera_shot, data_dir="data/frames"):
    annotation_dict = {"id": [], "x": [], "y": [], "side": []}
    for lot in camera_shot.lots:
        annotation_dict["id"].append(lot.id)
        annotation_dict["x"].append(lot.x)
        annotation_dict["y"].append(lot.y)
        annotation_dict["side"].append(lot.side)
    
    annotation_df = pd.DataFrame(annotation_dict)
    annotation_df["img_path"] = Path(data_dir).joinpath(camera_shot.img_path)

    dataset = ParkingLotDataset(annotation_df)
    dataloader = DataLoader(dataset, batch_size=16, drop_last=False, collate_fn=collate_fn)
    
    return annotation_df, dataloader
