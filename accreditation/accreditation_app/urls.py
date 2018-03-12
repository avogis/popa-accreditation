from django.conf.urls import url
from accreditation_app import views


urlpatterns = [
    url(r'^application_accepted/$', views.application_accepted, name='application_accepted'),
]
