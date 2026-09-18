import numpy as np
import torch
from PIL import Image
from ultralytics import YOLO
from transformers import CLIPProcessor, CLIPModel
import faiss

_yolo = None
_clip = None
_clip_proc = None
_index = None
_id_map = []


def _load():
    global _yolo, _clip, _clip_proc
    if _yolo is None:
        _yolo = YOLO("yolov8n.pt")
    if _clip is None:
        _clip = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").eval()
        _clip_proc = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")


def embed_image(pil_img: Image.Image) -> np.ndarray:
    _load()
    inputs = _clip_proc(images=pil_img, return_tensors="pt")
    with torch.no_grad():
        feat = _clip.get_image_features(**inputs)
    feat = feat / feat.norm(p=2, dim=-1, keepdim=True)
    return feat.cpu().numpy().astype("float32")[0]


def detect_objects(pil_img, conf=0.35):
    _load()
    results = _yolo(pil_img, conf=conf, verbose=False)[0]
    boxes = []
    for b in results.boxes:
        x1, y1, x2, y2 = b.xyxy[0].tolist()
        label = results.names[int(b.cls[0])]
        boxes.append((label, float(b.conf[0]), (int(x1), int(y1), int(x2), int(y2))))
    return boxes


def build_index(products):
    global _index, _id_map
    vecs, ids = [], []
    for p in products:
        if p.embedding:
            vecs.append(np.frombuffer(p.embedding, dtype="float32"))
            ids.append(p.id)
    if not vecs:
        _index, _id_map = None, []
        return
    mat = np.vstack(vecs).astype("float32")
    _index = faiss.IndexFlatIP(mat.shape[1])
    _index.add(mat)
    _id_map = ids


def search_similar(vec, top_k=4):
    if _index is None:
        return []
    D, I = _index.search(vec.reshape(1, -1), top_k)
    return [(_id_map[i], float(d)) for i, d in zip(I[0], D[0]) if i != -1]