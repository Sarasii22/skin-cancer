import numpy as np
from skimage.measure import label, regionprops

def calculate_abcd(image_pil, mask_pil):
    img = np.array(image_pil)
    mask = np.array(mask_pil) > 128
    if not mask.any():
        return 0.0, {"A":0,"B":0,"C":0,"D":0,"Total":0}

    labels = label(mask)
    props = max(regionprops(labels), key=lambda x: x.area, default=None)
    if not props: return 0.0, {"A":0,"B":0,"C":0,"D":0,"Total":0}

    A = 1.3
    B = max(0, (props.perimeter**2 / (4 * 3.14 * props.area) - 1) * 10)
    C = np.std(cv2.cvtColor(img, cv2.COLOR_RGB2HSV)[mask, 2]) / 255 * 3
    D = min(props.major_axis_length / 30, 2.0)

    total = A + B + C + D
    return round(total, 2), {
        "A": round(A,2), "B": round(B,2), "C": round(C,2), "D": round(D,2), "Total": total
    }