from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from PIL import Image
from io import BytesIO
import uuid, os
from inference import predict, segment_lesion
from abcd import calculate_abcd
from report import generate_pdf

app = FastAPI(title="Skin Cancer Detector")
app.mount("/results", StaticFiles(directory="results"), name="results")
os.makedirs("results", exist_ok=True)

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    contents = await file.read()
    img = Image.open(BytesIO(contents)).convert("RGB")

    is_cancer, confidence, risk = predict(img)
    highlighted, mask = segment_lesion(img)
    abcd_score, abcd_details = calculate_abcd(img, mask)

    rid = str(uuid.uuid4())
    folder = f"results/{rid}"
    os.makedirs(folder, exist_ok=True)

    img.save(f"{folder}/original.jpg")
    highlighted.save(f"{folder}/highlighted.jpg")
    mask.save(f"{folder}/mask.png")

    generate_pdf(folder, {
        "is_cancer": is_cancer,
        "confidence": confidence,
        "risk": risk,
        "abcd_score": abcd_score,
        "abcd": abcd_details
    })

    return {
        "result_id": rid,
        "cancer": is_cancer,
        "confidence": confidence,
        "risk": risk,
        "abcd_score": abcd_score,
        "urls": {
            "original": f"/results/{rid}/original.jpg",
            "highlighted": f"/results/{rid}/highlighted.jpg",
            "report": f"/results/{rid}/report.pdf"
        }
    }