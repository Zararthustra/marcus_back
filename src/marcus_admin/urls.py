from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("marcus.urls")),
    path("api/music/", include("marcus_music.urls")),
]
