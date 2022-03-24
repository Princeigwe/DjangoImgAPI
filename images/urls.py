from django.urls import path
from .views import ImageListCreate, ImageRetrieveDestroyDetailView

app_name='images'

urlpatterns = [
    path('', ImageListCreate.as_view(), name="list_images"),
    path('<int:pk>/', ImageRetrieveDestroyDetailView.as_view(), name="image_detail")
]