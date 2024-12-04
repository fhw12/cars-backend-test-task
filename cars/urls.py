from django.urls import include, path
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'cars', views.CarViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'user-detail', views.UserViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.indexView, name='index'),
    path('car/<int:car_id>', views.carView, name='car details')
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]