from django.urls import path
from .views import ImageListCreate, ImageRetrieveDestroyDetailView

app_name='images'

urlpatterns = [
    path('list-images/', ImageListCreate.as_view(), name="list_images"),
    path('image-detail/<int:pk>/', ImageRetrieveDestroyDetailView.as_view(), name="image_detail")
]