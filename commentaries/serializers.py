from django.utils import timezone
from rest_framework.serializers import ModelSerializer, DateTimeField

from commentaries.models import Commentary, SubComment


class CommentarySerializer(ModelSerializer):

    class Meta:
        model = Commentary
        fields = ('id', 'timestamp', 'body')


class SubCommentSerializer(ModelSerializer):

    class Meta:
        model = SubComment
        fields = ('commentary', 'timestamp', 'body')


class SubCommentMinSerializer(ModelSerializer):

    class Meta:
        model = SubComment
        fields = ('timestamp', 'body')


class CommentaryWithSubsSerializer(ModelSerializer):
    sub_comment = SubCommentMinSerializer(many=True)

    class Meta:
        model = Commentary
        fields = ('sub_comment',)
