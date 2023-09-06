from django.urls import path

from lottery import admin


urlpatterns = [
    path('', admin.site.urls),
]
