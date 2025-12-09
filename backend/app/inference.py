from PIL import Image
import torch
from torchvision import transforms
import numpy as np
import cv2
from model import MODEL, DEVICE

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def predict(image_pil):
    img = transform(image_pil).unsqueeze(0).to(DEVICE)
    with torch.no_grad():
        out = MODEL(img)
        prob = torch.softmax(out, dim=1)[0][1].item()
    is_cancer = prob > 0.5
    risk = "High" if prob > 0.8 else "Moderate" if prob > 0.4 else "Low"
    return is_cancer, round(prob*100, 1), risk

def segment_lesion(image_pil):
    img = np.array(image_pil)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    _, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25,25))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    overlay = img.copy()
    overlay[mask == 255] = [255, 0, 0]
    result = cv2.addWeighted(img, 0.65, overlay, 0.35, 0)
    return Image.fromarray(result), Image.fromarray((mask*255).astype(np.uint8))