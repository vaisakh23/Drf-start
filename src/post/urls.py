from django.urls import path
from .views import (TestView, 
                    PostView, 
                    PostListView,
                    PostCreateView,
                    PostListCreateView,
                    PostRUDView,
                    PostOwnerView
                )


urlpatterns = [
    path('test-view/<int:pk>', TestView.as_view()),
    path('all-post', PostListView.as_view()),
    path('post/<int:pk>', PostRUDView.as_view()),
    path('post-owner/<int:pk>', PostOwnerView.as_view()),
    #path('post-view', PostView.as_view()),
    #path('post-create-view', PostCreateView.as_view()),
    #path('post-list-create-view', PostListCreateView.as_view()),
    #path('post-list-create-view/<int:pk>', PostListCreateView.as_view()),
]
