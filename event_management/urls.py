from django.contrib import admin
from django.urls import path, include
from core.views import home, no_permission
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('events/', include('events.urls')),
    path('users/', include('users.urls')),
    path('', home, name="home"),
    path('no-permission/', no_permission, name='no-permission')
]

# This should be outside any DEBUG condition since you need media files in production too
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)