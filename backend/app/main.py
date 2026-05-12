from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.datasets.router import router as datasets_router

app = FastAPI(title="Akriti API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "Akriti backend running"}

@app.get("/ping")
def ping():
    return {"message": "Akriti backend reachable"}

# ✅ ADD THIS
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "status": "uploaded successfully"
    }

app.include_router(datasets_router, prefix="/datasets")
