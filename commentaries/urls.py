from django.urls import path

from .views import CommentaryListApiView, SubCommentCreateApiView, CommentaryRetrieveApiView

urlpatterns = [
    path('commentary/', CommentaryListApiView.as_view(), name='commentary'),
    path('commentary/<int:pk>', CommentaryRetrieveApiView.as_view(), name='retrieve-comment'),
    path('add-sub/', SubCommentCreateApiView.as_view(), name='add-sub'),
]
