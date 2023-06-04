from django.urls import path
from .views import ProductAPI

app_name = 'api'

urlpatterns = [
    # path('', HomeView.as_view(), name='home'),
    path('products/', ProductAPI.as_view(), name='get-all-products')
]
