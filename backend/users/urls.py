from django.urls import path 
from .views import *

urlpatterns = [
    path('login/', loginView.as_view(), name='Login API'),
    path('register/',registration.as_view(),name='Registration'),
    # path('logout/', Logout.as_view(), name='Logout User'),
    path('logout/',LogoutView.as_view()),
    path('changepassword/', ChangePasswordView.as_view(), name='Change Password'),
    path('getcurrentuser/', getCurrentUserView.as_view(), name='Get Current User'),
    path('getallusers/', getallusersView.as_view(), name='Get All User'),
    path('getallusers/<int:id>/', getallusersView.as_view(), name='Get All User'),
]