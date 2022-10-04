"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from pes_admin.admin import custom_pes_admin_site
from django.views.static import serve

admin.autodiscover()

urlpatterns = [
    path('admin/advanced/', custom_pes_admin_site.urls),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.presentation.urls', namespace='accounts')),
    path('', include('application.presentation.urls',
         namespace='applications')),
    path('organization-subscription/',
         include(
             'organization_subscription.presentation.urls',
             namespace='organization_subscription')),
    path(
        'eligibility/',
        include('eligibility.presentation.urls', namespace='eligibility')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('staff/', include('staff.presentation.urls', namespace='staff')),
    path('agripitch/', include('agripitch.presentation.urls', namespace='agripitch')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.CPANEL_HOSTING:
    urlpatterns.append(re_path(r'^media/(?P<path>.*)$', serve,
                               {'document_root': settings.MEDIA_ROOT}))
    urlpatterns.append(
        re_path(r'^static/(?P<path>.*)$', serve,
                {'document_root': settings.STATIC_ROOT}))

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
