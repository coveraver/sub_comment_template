from django.test import TestCase
from django.utils.timezone import now, pytz
from django.conf import settings

from commentaries.models import Commentary, SubComment
from commentaries.serializers import (
    CommentarySerializer, SubCommentSerializer,
    SubCommentMinSerializer, CommentaryWithSubsSerializer
)


class CommentSerializerConsistentTestCase(TestCase):
    def setUp(self) -> None:
        self.comment_1 = Commentary.objects.create(
            body='Best comment for testing'
        )
        self.sub_comment = SubComment.objects.create(
            commentary_id=self.comment_1.id,
            body='Sub comment for best comment ever!'
        )
        self.settings_timezone = pytz.timezone(settings.TIME_ZONE)
        self.comments_timezone = now().astimezone(self.settings_timezone)
        self.data = [
            {
                'id': self.comment_1.id,
                'body': 'Best comment for testing'
            }
        ]

    def test_consistent(self) -> None:
        serializer_data = CommentarySerializer(self.comment_1)

        self.assertEqual([{'id': serializer_data.data['id'], 'body': serializer_data.data['body']}],
                         self.data)

    def test_commentary_with_subs_consistent(self) -> None:
        serializer_data = CommentaryWithSubsSerializer(self.comment_1)

        self.assertEqual(serializer_data.data['sub_comment'][0]['body'], 'Sub comment for best comment ever!')


class SubCommentSerializerConsistentTestCase(TestCase):
    def setUp(self) -> None:
        self.comment_1 = Commentary.objects.create(
            body='Best comment for testing'
        )
        self.comment_2 = Commentary.objects.create(
            body='Comment is about nothing'
        )
        self.sub_comment_1 = SubComment.objects.create(
            commentary_id=self.comment_1.id,
            body='Sub 1'
        )
        self.sub_comment_2 = SubComment.objects.create(
            commentary_id=self.comment_2.id,
            body='Sub 2'
        )

        self.settings_timezone = pytz.timezone(settings.TIME_ZONE)
        self.sub_comments_timezone = now().astimezone(self.settings_timezone)
        self.data = [
            {
                'commentary': self.comment_1.id,
                'body': 'Sub 1'
            }
        ]
        self.min_data = [
            {
                'body': 'Sub 2'
            }
        ]

    def test_consistent(self) -> None:
        serializer_data = SubCommentSerializer(self.sub_comment_1)

        self.assertEqual([{'commentary': 1, 'body': serializer_data.data['body']}], self.data)

    def test_min_serializer_consistent(self) -> None:
        serializer_data = SubCommentMinSerializer(self.sub_comment_2)

        self.assertEqual([{'body': serializer_data.data['body']}], self.min_data)
