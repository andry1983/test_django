from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path

apps_url = [
    re_path(r'^', include('apps.users.urls'))
]

urlpatterns_api = [
    re_path(r'^', include('apps.users.urls'))
]

urlpatterns = apps_url + static(settings.STATIC_URL,
                                document_root=settings.STATIC_ROOT)

if settings.DJANGO_ADMIN:
    urlpatterns += [path('admin/', admin.site.urls)]

if settings.DEBUG:
    if settings.USE_DEBUG_TOOLBAR:
        import debug_toolbar

        urlpatterns += [
            re_path(r'^__debug__/', include(debug_toolbar.urls)),
        ]

    if settings.USE_SILK:
        urlpatterns += [
            re_path(r'^silk/', include('silk.urls', namespace='silk'))
        ]

handler403 = 'core.views.handler403'
handler404 = 'core.views.handler404'
handler500 = 'core.views.handler500'
