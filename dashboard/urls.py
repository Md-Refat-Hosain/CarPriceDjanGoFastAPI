from django.contrib import admin
from django.urls import path
from dashboard.views import predict_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", predict_view, name="predict"),
]
