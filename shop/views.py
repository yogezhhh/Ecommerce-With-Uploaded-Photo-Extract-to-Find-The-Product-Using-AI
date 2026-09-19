import base64
from io import BytesIO
from PIL import Image, ImageDraw
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from django.db.models import Q

from .models import Product, Category, Order, OrderItem
from .cart import Cart
from .forms import RegisterForm, CheckoutForm
from .lens_engine import detect_objects, embed_image, embed_text, build_index, search_similar


def _data_url(img: Image.Image) -> str:
    buf = BytesIO()
    img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def home(request):
    featured = Product.objects.filter(is_featured=True)[:8]
    if not featured:
        featured = Product.objects.all()[:8]
    return render(request, 'shop/home.html', {
        'featured_products': featured,
        'categories': Category.objects.all(),
    })


def product_list(request):
    qs = Product.objects.all()
    q = request.GET.get('q')
    cat = request.GET.get('category')
    sort = request.GET.get('sort')
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))
    if cat:
        qs = qs.filter(category__slug=cat)
    if sort == 'price_asc':
        qs = qs.order_by('price')
    elif sort == 'price_desc':
        qs = qs.order_by('-price')
    return render(request, 'shop/product_list.html', {
        'products': qs,
        'categories': Category.objects.all(),
        'q': q or '',
        'active_cat': cat or '',
        'sort': sort or '',
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:4]
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'related': related,
    })


def cart_detail(request):
    return render(request, 'shop/cart.html', {'cart': Cart(request)})


def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    qty = int(request.POST.get('qty', 1))
    Cart(request).add(product, qty)
    messages.success(request, f"{product.name} added to cart")
    return redirect(request.META.get('HTTP_REFERER', 'cart'))


def cart_remove(request, product_id):
    Cart(request).remove(product_id)
    return redirect('cart')


def cart_update(request, product_id):
    qty = int(request.POST.get('qty', 1))
    Cart(request).update(product_id, qty)
    return redirect('cart')


def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('product-list')
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                full_name=form.cleaned_data['full_name'],
                email=form.cleaned_data['email'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                postal_code=form.cleaned_data['postal_code'],
                total=cart.total(),
            )
            for item in cart:
                OrderItem.objects.create(
                    order=order, product=item['product'],
                    price=item['price'], quantity=item['qty'],
                )
            cart.clear()
            messages.success(request, "Order placed!")
            return redirect('order-success', pk=order.pk)
    else:
        form = CheckoutForm(initial={
            'full_name': request.user.get_full_name() or request.user.username if request.user.is_authenticated else '',
            'email': request.user.email if request.user.is_authenticated else '',
        })
    return render(request, 'shop/checkout.html', {'cart': cart, 'form': form})


def order_success(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'shop/order_success.html', {'order': order})


def orders(request):
    if request.user.is_authenticated:
        user_orders = Order.objects.filter(user=request.user)
    else:
        user_orders = Order.objects.none()
    return render(request, 'shop/orders.html', {'orders': user_orders})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'shop/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def lens(request):
    context = {'mode': 'image'}
    text_q = request.GET.get('q')
    if text_q:
        context.update({'mode': 'text', 'text_query': text_q, 'text_matches': []})
        return render(request, 'shop/lens.html', context)

    if request.method == 'POST' and request.FILES.get('image'):
        query = Image.open(request.FILES['image']).convert('RGB')
        detections = detect_objects(query)
        regions = []
        for label, conf, (x1, y1, x2, y2) in detections:
            crop = query.crop((x1, y1, x2, y2))
            if crop.width < 20 or crop.height < 20:
                continue
            regions.append({
                'label': label,
                'confidence': round(conf, 3),
                'crop_data_url': _data_url(crop),
                'matches': [],
            })
        annotated = query.copy()
        draw = ImageDraw.Draw(annotated)
        for label, conf, (x1, y1, x2, y2) in detections:
            draw.rectangle([x1, y1, x2, y2], outline='lime', width=3)
        context.update({
            'mode': 'image',
            'annotated': _data_url(annotated),
            'regions': regions,
            'num_objects': len(regions),
        })
    return render(request, 'shop/lens.html', context)