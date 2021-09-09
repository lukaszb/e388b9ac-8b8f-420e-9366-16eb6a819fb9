"""swheros URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import views
from django.urls import path, re_path

urlpatterns = [
    path(r'', views.html_app),
    path('api/collections', views.collection_list),
    path('api/collections/create', views.collection_create),
    path('api/collections/<uuid:collection_id>', views.collection_details),
    path('api/collections/<uuid:collection_id>/data', views.collection_data),
    path('api/collections/<uuid:collection_id>/data/distinct', views.collection_data_distinct),
]
