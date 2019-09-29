from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from core.views import *
from rest_framework.authtoken import views

router = routers.DefaultRouter()
router.register(r'user', UserViewSet, basename='user')
router.register(r'stores', StoreViewSet, basename='country')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'connectors', ConnectorViewSet, basename='connector')


urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-token-auth/', views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls')),
    path('logout/', Logout.as_view()),
    #
    path('check-username/', CheckUsername.as_view()),
    path('check-email/', CheckEmail.as_view())
]
