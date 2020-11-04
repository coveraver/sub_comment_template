import json

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

from commentaries.models import Commentary, SubComment
from commentaries.serializers import SubCommentSerializer


class CommentApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.url = reverse('commentary')
        self.commentary_1 = Commentary.objects.create(body='Best comment for testing')
        self.commentary_2 = Commentary.objects.create(body='Comment is about nothing')
        self.sub_comment_1 = SubComment.objects.create(commentary=self.commentary_1,
                                                       body='Sub comment for commentary with ID 1')
        self.sub_comment_2 = SubComment.objects.create(commentary=self.commentary_2,
                                                       body='Sub 2 for comment with ID 2')

    def test_get(self) -> None:
        response: Response = self.client.get(self.url)
        data = {'comments': Commentary.objects.all()}

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(list(data['comments']), list(response.data['comments']))

    def test_detail(self) -> None:
        response: Response = self.client.get(f'{self.url}1')
        serializer_data = SubCommentSerializer(self.sub_comment_1)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual([1, 'Sub comment for commentary with ID 1'],
                         [serializer_data.data['commentary'], serializer_data.data['body']])
        self.assertEqual(1, SubComment.objects.filter(commentary_id=1).count())
        self.assertEqual(1, Commentary.objects.filter(sub_comment=self.sub_comment_1).count())

    def test_detail_invalid_pk(self):
        response: Response = self.client.get(f'{self.url}3')

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class AddSubCommentTestCase(APITestCase):
    def setUp(self) -> None:
        self.valid_data = json.dumps({
            'commentary': '1',
            'body': 'perfecto!'
        })
        self.invalid_data = json.dumps({
            'body': 'no perfecto!'
        })
        self.data_with_invalid_comment_id = json.dumps({
            'commentary': '2',
            'body': 'un perfecto!'
        })
        self.empty_data = json.dumps({

        })
        Commentary.objects.create(body='Please comment me!')
        self.user = get_user_model().objects.create_user('tester')
        self.url = reverse('add-sub')

    def test_valid_create(self) -> None:
        self.client.force_login(self.user)
        response: Response = self.client.post(self.url, data=self.valid_data, content_type='application/json')
        serializer_data = SubCommentSerializer(SubComment.objects.first())

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, SubComment.objects.all().count())
        self.assertEqual('perfecto!', serializer_data.data['body'])

    def test_invalid_create(self) -> None:
        self.client.force_login(self.user)
        response: Response = self.client.post(self.url, data=self.invalid_data, content_type='application/json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_invalid_comment_id(self) -> None:
        self.client.force_login(self.user)
        response: Response = self.client.post(self.url, data=self.data_with_invalid_comment_id,
                                              content_type='application/json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_unauthorized(self) -> None:
        response: Response = self.client.post(self.url, data=self.valid_data, content_type='application/json')

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_empty_data(self) -> None:
        self.client.force_login(self.user)
        response: Response = self.client.post(self.url, data=self.empty_data, content_type='application/json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
