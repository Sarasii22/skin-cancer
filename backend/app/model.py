import torch
import torch.nn as nn

def load_model():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    try:
        model = torch.load("models/your_model.pth", map_location=device)
    except:
        import torchvision.models as models
        model = models.resnet50(pretrained=False)
        model.fc = nn.Linear(model.fc.in_features, 2)
        state = torch.load("models/your_model.pth", map_location=device)
        model.load_state_dict(state if isinstance(state, dict) else state.state_dict())
    model.eval()
    model.to(device)
    return model, device

MODEL, DEVICE = load_model()