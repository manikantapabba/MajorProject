from django.urls import path
from . import views

urlpatterns = [
    path('',views.signin,name="signin_page"),
    path('signup',views.signup,name="signup_page"),
    path('home',views.home,name="home_page"),
    path('logout',views.logout,name="logout_page"),
    path('uploads',views.uploads,name="uploads_page"),
    path('myuploads',views.myuploads,name="myuploads_page"),
    path('uploadstatus',views.uploadstatus,name="uploadstatus_page"),
    path('rate/<pk>',views.rate,name="rate_page"),
    path('yourratings',views.yourratings,name="yourratings_page"),
    path('ratings',views.ratings,name="ratings_page"),
    path('graphs/<chart_type>',views.graphs,name="graphs_page"),
]