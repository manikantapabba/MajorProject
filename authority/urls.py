from django.urls import path
from . import views

urlpatterns = [
    path('adsignin',views.adsignin,name="adsignin"),
    path('adhome',views.adhome,name="adhome"),
    path('updatestatus/<updatedetail>/<pk>',views.updatestatus,name="updatestatus"),
    path('developerrequests',views.developerrequests,name="developerrequests"),
    path('aduploaddata',views.aduploaddata,name="aduploaddata"),
    # path('preview/<filename>',views.preview,name="preview"),
    path('adratings',views.adratings,name="adratings"),
    path('adlogout',views.adlogout,name="adlogout"),

    
]