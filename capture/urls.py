from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^thanks/$', views.Thanks.as_view(), name='thanks'),
    url(r'^$', views.LeadDetailView.as_view(), name='lead'),
]
