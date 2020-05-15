"""news URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

from core.views import \
    Index, \
    PostDetail, \
    CreatePostViews, \
    TagPostViews, \
    PostDetailLike, \
    PostDetailUnlike, \
    PostTimeCreate, \
    ContactView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Index.as_view()),
    path('post/<int:pk>/like', PostDetailLike.as_view()),
    path('post/<int:pk>/unlike', PostDetailUnlike.as_view()),
    path('post/<int:pk>', PostDetail.as_view()),
    path('tag/<int:pk>', TagPostViews.as_view()),
    path('create/post', CreatePostViews.as_view()),
    path('create/post_time', PostTimeCreate.as_view()),
    path('contacts', ContactView.as_view()),
    path('accounts/', include('django_registration.backends.one_step.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
