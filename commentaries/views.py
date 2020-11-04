from django.http import HttpRequest
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from .models import Commentary, SubComment
from .serializers import SubCommentSerializer, CommentarySerializer, CommentaryWithSubsSerializer


class CommentaryListApiView(ListAPIView):
    serializer_class = CommentarySerializer
    template_name = 'comments.html'
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request: HttpRequest, *args, **kwargs) -> Response:
        data = {'comments': Commentary.objects.all()}
        return Response(data, template_name=self.template_name)


class CommentaryRetrieveApiView(RetrieveAPIView):
    queryset = Commentary.objects.all()
    serializer_class = CommentaryWithSubsSerializer


class SubCommentCreateApiView(CreateAPIView):
    queryset = SubComment.objects.all()
    serializer_class = SubCommentSerializer
