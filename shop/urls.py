from django.urls import path
from .views import category_version_view ,repuestos_view, accesorios_view ,en_construccion, category_view, about, cart_view, add_product, edit_product, delete_product, product_list, add_to_cart, remove_from_cart, update_cart, get_versions, product_detail, home, products_by_model
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", home, name="home"),
    path("add-product/", add_product, name="add_product"),
    path("products/model/<int:model_id>/", products_by_model, name="products_by_model"),
    path("products/<int:product_id>/", product_detail, name="product_detail"),
    path("cart/", cart_view, name="cart"),  # Asegura que está usando cart_view
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path("cart/remove/<int:item_id>/", remove_from_cart, name="remove_from_cart"),
    path("cart/update/<int:item_id>/", update_cart, name="update_cart"),
    path("products/edit/<int:product_id>/", edit_product, name="edit_product"),
    path("products/delete/<int:product_id>/", delete_product, name="delete_product"),
    path("about/", about, name="about"),
    path("categoria/<str:model>/<str:category>/", category_view, name="category_view"),
    # Nueva ruta para categoría filtrada por modelo y versión
    path("categoria/<str:model>/<str:category>/<int:version_id>/", category_version_view, name="category_version_view"),
    path('construccion/', en_construccion, name='en_construccion'),
    path("api/get_versions/", get_versions, name="get_versions"),
    path("products/", product_list, name="product_list"),
    path("repuestos/", repuestos_view, name="repuestos"),
    path("repuestos/<int:modelo_id>/", repuestos_view, name="repuestos_modelo"),
    path("repuestos/<int:modelo_id>/<int:version_id>/", repuestos_view, name="repuestos_version"),
    path("accesorios/", accesorios_view, name="accesorios"),
    path("accesorios/<int:modelo_id>/", accesorios_view, name="accesorios_modelo"),
    path("accesorios/<int:modelo_id>/<int:version_id>/", accesorios_view, name="accesorios_version"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

