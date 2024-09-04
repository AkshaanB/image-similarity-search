from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from project.routers import root, image_upload, retrieve_images


app = FastAPI(title="Image Search Application")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(root.router)
app.include_router(image_upload.router)
app.include_router(retrieve_images.router)
