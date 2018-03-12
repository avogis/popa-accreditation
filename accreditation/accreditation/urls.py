"""accreditation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from accreditation_app import views as accreditation_views
from accreditation_app import urls as accreditation_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', accreditation_views.accreditation_page, name='accreditation_page'),
    # url(r'^accreditation_app/', include(accreditation_urls)),
]
