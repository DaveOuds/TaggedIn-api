from django.conf.urls import url
from contact import views


from contact.views import ContactList

urlpatterns = [
    url(r'^contacts$', ContactList.as_view()),
    url(r'^contact/(?P<pk>[0-9]+)$', views.contact_detail)
]