from django.contrib import admin
from django.urls import path, include
from catalog import views as catalog_views  # ربط صريح لتطبيق الكتالوج
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # الصفحة الرئيسية (Home)
    path('', catalog_views.home, name='home'),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    # باقي مسارات التطبيقات
    path('catalog/', include('catalog.urls')),
    path('loans/', include('loans.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)