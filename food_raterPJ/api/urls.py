from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('meals', views.MealsView)
router.register('ratings', views.RateView)
urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.login_view),
    path('logout/', views.logout_view),
    path('get-users/', views.get_users),
    path('get-users/<int:pk>/', views.get_user),
]
