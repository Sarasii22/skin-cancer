from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from io import BytesIO
import uuid, os, cv2, numpy as np
import torch
from torchvision import transforms

app = FastAPI()

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve results folder
os.makedirs("results", exist_ok=True)
app.mount("/results", StaticFiles(directory="results"), name="results")

# Load your .pth model (works with any architecture)
device = torch.device("cpu")
try:
    model = torch.load("models/your_model.pth", map_location=device)
    if hasattr(model, 'eval'):
        model.eval()
except:
    import torchvision.models as models
    model = models.resnet50(pretrained=False)
    model.fc = torch.nn.Linear(model.fc.in_features, 2)
    state = torch.load("models/your_model.pth", map_location=device)
    model.load_state_dict(state if isinstance(state, dict) else state.state_dict())
    model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def predict_cancer(img_pil):
    img = transform(img_pil).unsqueeze(0)
    with torch.no_grad():
        out = model(img)
        prob = torch.softmax(out, dim=1)[0][1].item()
    return prob > 0.5, round(prob*100, 1), "High" if prob > 0.8 else "Moderate" if prob > 0.4 else "Low"

def segment_and_highlight(img_pil):
    img = np.array(img_pil)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    _, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (30,30))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    overlay = img.copy()
    overlay[mask == 255] = [255, 0, 0]
    result = cv2.addWeighted(img, 0.7, overlay, 0.3, 0)
    return Image.fromarray(result), Image.fromarray((mask*255).astype(np.uint8))

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    contents = await file.read()
    img = Image.open(BytesIO(contents)).convert("RGB")

    is_cancer, confidence, risk = predict_cancer(img)
    highlighted, mask = segment_and_highlight(img)

    rid = str(uuid.uuid4())
    folder = f"results/{rid}"
    os.makedirs(folder, exist_ok=True)

    img.save(f"{folder}/original.jpg")
    highlighted.save(f"{folder}/highlighted.jpg")
    mask.save(f"{folder}/mask.png")

    # Simple HTML report
    html = f"""
    <h1 style="color:red">SKIN CANCER REPORT</h1>
    <h2>Result: {'<span style="color:red">CANCER DETECTED</span>' if is_cancer else '<span style="color:green">BENIGN</span>'}</h2>
    <p><strong>Confidence:</strong> {confidence}% | <strong>Risk:</strong> {risk}</p>
    <img src="original.jpg" width="400"/>
    <img src="highlighted.jpg" width="400"/>
    """
    with open(f"{folder}/report.html", "w") as f:
        f.write(html)

    return {
        "cancer": is_cancer,
        "confidence": confidence,
        "risk": risk,
        "images": {
            "original": f"/results/{rid}/original.jpg",
            "highlighted": f"/results/{rid}/highlighted.jpg",
            "report": f"/results/{rid}/report.html"
        }
    }

@app.get("/")
def home():
    return {"message": "Skin Cancer API Running!"}