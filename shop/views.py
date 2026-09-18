from django.shortcuts import render, get_object_or_404
from .models import Product
import base64
from io import BytesIO
from PIL import Image, ImageDraw
from .lens_engine import detect_objects, embed_image, build_index, search_similar
from .models import Product


def _to_data_url(img: Image.Image) -> str:
    buf = BytesIO()
    img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def lens(request):
    context = {}
    if request.method == "POST" and request.FILES.get("image"):
        query = Image.open(request.FILES["image"]).convert("RGB")
        detections = detect_objects(query)

        build_index(Product.objects.exclude(embedding=None))

        regions = []
        for label, conf, (x1, y1, x2, y2) in detections:
            crop = query.crop((x1, y1, x2, y2))
            if crop.width < 20 or crop.height < 20:
                continue
            vec = embed_image(crop)
            matches = search_similar(vec, top_k=4)
            ids = [m[0] for m in matches]
            prods = {p.id: p for p in Product.objects.filter(id__in=ids)}
            regions.append({
                "label": label,
                "confidence": round(conf, 3),
                "crop_data_url": _to_data_url(crop),
                "matches": [{"product": prods[m[0]], "score": m[1]} for m in matches if m[0] in prods],
            })

        annotated = query.copy()
        draw = ImageDraw.Draw(annotated)
        for label, conf, (x1, y1, x2, y2) in detections:
            draw.rectangle([x1, y1, x2, y2], outline="lime", width=3)

        context = {
            "annotated": _to_data_url(annotated),
            "regions": regions,
            "num_objects": len(regions),
        }
    return render(request, 'shop/lens.html', context)


def home(request):
    featured = Product.objects.all().order_by('-created')[:4]
    return render(request, 'shop/home.html', {'featured_products': featured})


def product_list(request):
    products = Product.objects.all().order_by('-created')
    return render(request, 'shop/product_list.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})


def lens(request):
    # Google Lens page (backend AI added in Step 11)
    return render(request, 'shop/lens.html')