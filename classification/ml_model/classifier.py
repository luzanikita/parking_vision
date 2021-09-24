import torch
import torch.nn as nn
import torch.optim as optim
import pytorch_lightning as pl
from torchmetrics import functional as FM


class ParkingLotClassifier(pl.LightningModule):
    def __init__(self, model):
        super().__init__()
        self.criterion = nn.CrossEntropyLoss()
        self.model = model
    
    def forward(self, x):
        print(x.shape)
        x = self.model.forward(x)
        return x
    
    def configure_optimizers(self):
        optimizer = optim.SGD(
            self.parameters(),
            lr=0.01, # 0.01 -> 0.005 -> 0.0025
            momentum=0.9,
            weight_decay=0.0005
        )
        return optimizer
    
    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self.forward(x)
        loss = self.criterion(y_hat, y.long())
        self.log("train_loss", loss)
        return loss
    
    def validation_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self.forward(x)
        loss = self.criterion(y_hat, y.long())
        acc = FM.accuracy(y_hat, y)
        metrics = {'val_acc': acc, 'val_loss': loss}
        self.log_dict(metrics)
        return metrics

    def test_step(self, batch, batch_idx):
        metrics = self.validation_step(batch, batch_idx)
        metrics = {'test_acc': metrics['val_acc'], 'test_loss': metrics['val_loss']}
        self.log_dict(metrics)

    def predict_step(self, batch, batch_idx, dataloader_idx=None):
        x, y = batch
        y_hat = self.forward(x)
        return y_hat.argmax(dim=1)
