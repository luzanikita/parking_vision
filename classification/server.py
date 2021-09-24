from pathlib import Path

import uvicorn
from fastapi import APIRouter, Depends, FastAPI
from starlette.middleware.cors import CORSMiddleware

from utils import prepare_model, prepare_data, CameraShot


weights_path = "data/trained_model/puc.pth"
classifier, trainer = prepare_model(weights_path)

router = APIRouter()

@router.get("/")
def home():
    return {"message": "Health Check Passed!"}

@router.post('/predict')
def predict(camera_shot: CameraShot):
    annotation_df, dataloader = prepare_data(camera_shot, data_dir="data/frames")
    annotation_df["prediction"] = trainer.predict(classifier, dataloader)[0]
    response = {"statuses": []}
    for _, row in annotation_df.iterrows():
        status = {
            "lot_id": int(row["id"]),
            "is_free": not bool(row["prediction"])
        }
        response["statuses"].append(status)
    # Path(annotation_df.loc[0, "img_path"]).unlink()
    return response

app = FastAPI()
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5001)
