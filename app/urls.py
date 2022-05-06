from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers

router = routers.DefaultRouter()
router.register('bids', views.BidViewset, basename='bids')

urlpatterns = [
    path('', views.home, name='home'),
    path('section/<str:type>', views.section, name='section'),
    path('product/<int:id>', views.product, name='product'),
    path('sale/', views.sale, name='sale'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login_signin, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)