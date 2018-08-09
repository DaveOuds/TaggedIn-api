from django.contrib import admin
from django.conf.urls import url, include

urlpatterns = [
    url(r'^api/', include('contact.urls')),
    url(r'^api/', include('user.urls')),
    url(r'^admin/', admin.site.urls),
]
