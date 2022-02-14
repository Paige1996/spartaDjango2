"""sparta URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from typing import Dict

from django.contrib import admin
from django.http import HttpRequest
from django.urls import path
from ninja import NinjaAPI  # djangoNINJA에 api객체 import

api = NinjaAPI()


@api.get("/add")  # 닌자 사용. urls 와 view function이 분리된 형태가 아님. url로 가면 어떤 함수가 실행되는 지 바로 볼수있음
def add(request: HttpRequest, a: int, b: int) -> Dict[str, int]:
    return {"result": a + b}


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
print("Life is Tooooooo Short")
