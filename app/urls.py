from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('section/<str:type>', views.section, name='section'),
    path('product/', views.product, name='product'),
    path('sale/', views.sale, name='sale'),
    path('profile/', views.profile, name='profile'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)