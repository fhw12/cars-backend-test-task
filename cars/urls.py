from django.urls import include, path
from django.contrib.auth import views as auth_views
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'cars', views.CarViewSet)
router.register(r'user-detail', views.UserViewSet)


urlpatterns = [
    path('', views.index_view, name='index'),

    path('signin/', views.signin_view, name='signin'),
    path('signin/login/', views.login_view, name='login'),
    path('signup/reg/', views.reg_view, name='reg'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),

    path('car/<int:car_id>', views.car_view, name='car-details'),
    path('new-car/', views.new_car, name='new-car'),
    path('add-car/', views.add_car, name='add-car'),
    path('edit-car/<int:car_id>', views.edit_car, name='edit-car'),
    path('delete-car/<int:car_id>', views.delete_car, name='delete-car'),
    path('add-comment/<int:car_id>', views.add_comment, name='add-comment'),

    path('api/', include(router.urls)),
    path('api/cars/<int:car_id>/comments/', views.CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='car-comments'),
    path('api/comments/<int:pk>/', views.CommentViewSet.as_view({'get': 'retrieve'}), name='comment-detail'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]