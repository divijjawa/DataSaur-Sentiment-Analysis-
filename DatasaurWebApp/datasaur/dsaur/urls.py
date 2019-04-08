from django.urls import path

from . import views

urlpatterns = [
    path('',views.home),
    path('search', views.search),
    path('search/<query>', views.search),
    path('search/heatmap/<query>', views.heatsearch),
    path('datasaur/trending', views.trending),
    path('bhost/index',views.home),
    path('datasaur/trend/<query>', views.trendDetail),
    path('datasaur/trend/tweets/<query>',views.trendtweets),
    path('datasaur/trend/detail/<query>', views.trendtone)
]



