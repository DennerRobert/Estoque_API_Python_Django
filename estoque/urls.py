from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
	path('', include('apps.core.urls')),
	path('produto/', include('apps.produto.urls')),
	path('estoque/', include('apps.estoque_produtos.urls')),
	path('api/v1/', include('apps.api.urls')),
	path('admin/', admin.site.urls),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)