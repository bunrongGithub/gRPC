
from django.contrib import admin
from django.urls import path, include
from productservice.views import ProductInfoView, ProductListView

# from productservice.views import ProductInfoView,ProductList
urlpatterns = [
    path("api/products/<int:pk>", view=ProductInfoView.as_view()),
    path("api/products", view=ProductListView.as_view()),
    path("admin/", admin.site.urls),
    path("",include("orderservice.urls")),
    path("",include("paymentservice.urls"))
]
