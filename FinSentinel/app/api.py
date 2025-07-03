from fastapi import FastAPI, UploadFile, File
import pandas as pd
from io import StringIO

app = FastAPI()

@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_csv(StringIO(contents.decode()))
    return {"rows_uploaded": len(df)}
