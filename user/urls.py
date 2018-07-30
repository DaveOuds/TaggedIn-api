from django.conf.urls import url
from rest_auth.views import (
    LoginView, LogoutView, PasswordChangeView
)

from user.views import (
    RegisterView, DeleteUserView,
)

urlpatterns = [
    url(r'^login$', LoginView.as_view()),
    url(r'^logout$', LogoutView.as_view()),
    url(r'^register$', RegisterView.as_view()),
    url(r'^change_password', PasswordChangeView.as_view()),
    url(r'^delete_user', DeleteUserView.as_view())
]
