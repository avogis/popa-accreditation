from django.conf.urls import url
from accreditation_app import views


urlpatterns = [
    url(r'^$', views.accreditation_page, name='accreditation'),
]
