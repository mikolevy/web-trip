from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("trip-assistance-api/", include("trip_assistance.urls")),
]
