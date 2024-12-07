from django.urls import include, path
from django.contrib.auth import views as auth_views
from rest_framework import routers
from . import views


# router for API paths
router = routers.DefaultRouter()
router.register(r'cars', views.CarViewSet)
router.register(r'user-detail', views.UserViewSet)


urlpatterns = [
    # paths to views
    path('', views.index_view, name='index'),
    path('signin/', views.signin_view, name='signin'),
    path('signup/', views.signup_view, name='signup'),
    path('car/<int:car_id>', views.car_view, name='car-details'),
    path('new-car/', views.new_car, name='new-car'),

    # paths to handlers
    path('signin/login/', views.login_handler, name='login'),
    path('signup/reg/', views.reg_handler, name='reg'),
    path('logout/', views.logout_handler, name='logout'),
    path('add-car/', views.add_car_handler, name='add-car'),
    path('update-car/<int:car_id>', views.update_car_handler, name='update-car'),
    path('delete-car/<int:car_id>', views.delete_car_handler, name='delete-car'),
    path('add-comment/<int:car_id>', views.add_comment_handler, name='add-comment'),

    # api paths
    path('api/', include(router.urls)),
    path('api/cars/<int:car_id>/comments/', views.CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='car-comments'),
    path('api/comments/<int:pk>/', views.CommentViewSet.as_view({'get': 'retrieve'}), name='comment-detail'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]