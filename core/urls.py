from django.urls import path
from .views import HomePage
from . import views

app_name = "core"
urlpatterns = [
    path('', HomePage.as_view(), name="cat-home"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register, name="register"),
    path('vote/<int:id>/', views.vote, name="vote"),
    path('<str:slug>/', views.detail, name="detail")
]