from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from .models import Cart, CartItem, Product, ModelCar, CarVersion
from .forms import ProductForm

# Página principal
def home(request):
    models = ModelCar.objects.prefetch_related('versions').all()
    return render(request, "shop/home.html", {"models": models})

# Filtrar productos por modelo de auto
def products_by_model(request, model_id):
    model = get_object_or_404(ModelCar, id=model_id)
    products = Product.objects.filter(compatible_models=model)  # ✅ Filtrar por modelos compatibles
    return render(request, "shop/products.html", {"products": products, "model": model})

# Página de detalles de un producto
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/product_detail.html', {'product': product})

# Página del carrito de compras
@login_required
@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Lista de vendedores con nombre y número de WhatsApp
    vendedores = [
        {"nombre": "Fernanda Alvarez", "telefono": "+5491123050766"},
        {"nombre": "Kerry Forney", "telefono": "+549115338-7060"},
        {"nombre": "Carlos Barra", "telefono": "+5491131619106"},
        {"nombre": "Rodrigo Zaccardi", "telefono": "+5491123466172"},
    ]

    return render(request, "shop/cart.html", {"cart": cart, "vendedores": vendedores})

# Agregar un producto al carrito
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')

# Eliminar un producto del carrito
@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect("cart")

# Actualizar cantidad en el carrito
@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if request.method == "POST":
        quantity = request.POST.get("quantity")
        cart_item.quantity = int(quantity) if quantity.isdigit() and int(quantity) > 0 else 1
        cart_item.save()

    return redirect("cart")

# Validar si el usuario es administrador
def is_admin(user):
    return user.is_authenticated and user.is_staff

# Agregar producto

@login_required
def add_product(request):
    if not request.user.is_staff:
        return redirect("home")  # Redirige si el usuario no es administrador

    categories = Product.CATEGORY_CHOICES  # Categorías del producto
    models = ModelCar.objects.all()  # Modelos de autos
    versions = CarVersion.objects.all()  # Versiones de autos

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("product_list")  # Redirige a la lista de productos
    else:
        form = ProductForm()

    return render(request, "shop/add_product.html", {
        "form": form,
        "categories": categories,
        "models": models,  # Se pasa la lista de modelos a la plantilla
        "versions": versions  # Se pasa la lista de versiones a la plantilla
    })
# Editar producto
@user_passes_test(is_admin)
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    categories = Product.objects.values_list('category', flat=True).distinct()  # Obtiene las categorías únicas

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = ProductForm(instance=product)

    return render(request, "shop/edit_product.html", {
        "form": form,
        "categories": categories,
    })

# Eliminar producto
@user_passes_test(is_admin)
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        product.delete()
        return redirect("product_list")

    return render(request, "shop/delete_product.html", {"product": product})

# Listar productos y filtrar por versión
def product_list(request):
    version_id = request.GET.get('version')  # Obtiene la versión seleccionada desde la URL
    products = Product.objects.all()  # Por defecto, muestra todos los productos

    if version_id:  # Si se seleccionó una versión, filtrar los productos
        products = products.filter(versions__id=version_id)  # ✅ Corrección aquí

    versions = CarVersion.objects.all()  # Obtener todas las versiones para el dropdown

    return render(request, 'shop/product_list.html', {
        'products': products,
        'versions': versions,
        'selected_version': version_id
    })

# Vista de categorías y modelos
def category_view(request, model_name, category_name, version_id=None):
    """Filtra los productos por modelo de auto, categoría y versión (opcional)"""

    # Filtrar productos por modelo y categoría
    products = Product.objects.filter(category=category_name, compatible_models__name=model_name)

    # Si se proporciona una versión, filtrar aún más
    if version_id:
        products = products.filter(versions__id=version_id)

    # Obtener todas las versiones disponibles para el modelo seleccionado
    model = get_object_or_404(ModelCar, name=model_name)
    versions = CarVersion.objects.filter(model=model)

    return render(request, "shop/category.html", {
        "products": products,
        "category": category_name,
        "model": model_name,
        "versions": versions,  # Enviar versiones para mostrarlas en el submenú
    })
# Página "Acerca de"
def about(request):
    return render(request, "shop/about.html")

# Vista para manejar error 403
def error_403(request, exception):
    return render(request, "shop/403.html", status=403)

# Página en construcción
def en_construccion(request):
    return render(request, 'shop/en_construccion.html')

# Obtener versiones según modelo seleccionado
def get_versions(request):
    model_id = request.GET.get("model_id")
    if model_id:
        versions = CarVersion.objects.filter(model_id=model_id).values("id", "name")
        return JsonResponse({"versions": list(versions)}, safe=False)
    return JsonResponse({"versions": []}, safe=False)


from django.shortcuts import render, get_object_or_404
from .models import Product, ModelCar, CarVersion

def repuestos_view(request, modelo_id=None, version_id=None):
    """ Filtra solo repuestos por modelo y versión del auto """
    productos = Product.objects.filter(category="Repuestos")

    if modelo_id:
        modelo = get_object_or_404(ModelCar, id=modelo_id)
        productos = productos.filter(compatible_models=modelo)
    else:
        modelo = None

    if version_id:
        version = get_object_or_404(CarVersion, id=version_id)
        productos = productos.filter(versions=version)
    else:
        version = None

    modelos = ModelCar.objects.all()
    versiones = CarVersion.objects.all()

    return render(request, "shop/repuestos.html", {
        "productos": productos,
        "modelos": modelos,
        "versiones": versiones,
        "modelo_seleccionado": modelo,
        "version_seleccionada": version,
    })


def accesorios_view(request, modelo_id=None, version_id=None):
    """ Filtra solo accesorios por modelo y versión del auto """
    productos = Product.objects.filter(category="Accesorios")

    if modelo_id:
        modelo = get_object_or_404(ModelCar, id=modelo_id)
        productos = productos.filter(compatible_models=modelo)
    else:
        modelo = None

    if version_id:
        version = get_object_or_404(CarVersion, id=version_id)
        productos = productos.filter(versions=version)
    else:
        version = None

    modelos = ModelCar.objects.all()
    versiones = CarVersion.objects.all()

    return render(request, "shop/accesorios.html", {
        "productos": productos,
        "modelos": modelos,
        "versiones": versiones,
        "modelo_seleccionado": modelo,
        "version_seleccionada": version,
    })

# Vista para la página de Repuestos filtrada por modelo y versión
def repuestos_view(request, model_id=None, version_id=None):
    products = Product.objects.filter(category="repuestos")

    if model_id:
        products = products.filter(compatible_models__id=model_id)
    if version_id:
        products = products.filter(versions__id=version_id)

    models = ModelCar.objects.all()
    versions = CarVersion.objects.all()

    return render(request, "shop/repuestos.html", {
        "products": products,
        "models": models,
        "versions": versions,
        "selected_model": model_id,
        "selected_version": version_id
    })

# Vista para la página de Accesorios filtrada por modelo y versión
def accesorios_view(request, model_id=None, version_id=None):
    products = Product.objects.filter(category="accesorios")

    if model_id:
        products = products.filter(compatible_models__id=model_id)
    if version_id:
        products = products.filter(versions__id=version_id)

    models = ModelCar.objects.all()
    versions = CarVersion.objects.all()

    return render(request, "shop/accesorios.html", {
        "products": products,
        "models": models,
        "versions": versions,
        "selected_model": model_id,
        "selected_version": version_id
    })

def category_version_view(request, model, category, version_id):
    print(f"Modelo: {model}, Categoría: {category}, Versión ID: {version_id}")  # 🛠 Verifica si llegan datos correctos

    model_obj = get_object_or_404(ModelCar, name=model)
    version_obj = get_object_or_404(CarVersion, id=version_id, model=model_obj)

    products = Product.objects.filter(compatible_models=model_obj, category=category, versions=version_obj)

    versions = CarVersion.objects.filter(model=model_obj)

    return render(request, "shop/category.html", {
        "category": category,
        "model": model,
        "selected_version": version_obj,
        "products": products,
        "versions": versions
    })

