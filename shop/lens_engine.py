# shop/lens_engine.py  — TEMPORARY STUB (no AI)
import numpy as np
from PIL import Image


def embed_image(pil_img: Image.Image) -> np.ndarray:
    """Placeholder — returns random vector. Replace with CLIP later."""
    return np.random.rand(512).astype("float32")


def embed_text(text: str) -> np.ndarray:
    return np.random.rand(512).astype("float32")


def detect_objects(pil_img, conf=0.35):
    """Placeholder — treats whole image as one object."""
    w, h = pil_img.size
    return [("object", 0.9, (0, 0, w, h))]


def build_index(products):
    pass


def search_similar(vec, top_k=4):
    return []