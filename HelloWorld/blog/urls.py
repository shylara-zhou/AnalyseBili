from django.urls import path,re_path
from blog import views
from blog import draw
urlpatterns=[
   path('hello/',views.hello), 
   path('getdata',views.getdata),
   path('',views.hello),
   path('drawcipin',views.drawcipin),
   path('tryit',views.tryit)
]