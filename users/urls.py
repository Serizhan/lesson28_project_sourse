
from django.urls import path
from rest_framework import routers

from users import views

urlpatterns = [
    path('', views.UserListView.as_view()),
    path('<int:pk>', views.UserRetrieveView.as_view()),
    path('<int:pk>/update', views.UserUpdateView.as_view()),
    path('<int:pk>/delete', views.UserDestroyView.as_view()),
    path('create/', views.UserCreateView.as_view()),
]

