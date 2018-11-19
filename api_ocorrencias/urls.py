from django.urls import path, include

from core.api.swagger import schema_view

urlpatterns = [
    path('api/', include('core.api.router')),
    path('', schema_view),
]
