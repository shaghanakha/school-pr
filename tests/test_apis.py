from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from exercise.models import Lesson, News
from exercise.models import User


class AccountsTest(APITestCase):
    def setUp(self):
        self.register_url = reverse("t_register")
        self.login_url = reverse("login")

        self.user_data = {
            "username": "user1",
            "first_name": "fname",
            "last_name": "lname",
            "password": "randompass",
            "national_code": "4343434343",
            "school_name": "schoolname",
            "lesson_name": "lessonname",
        }
        self.user_data2 = {
            "username": "user2",
            "first_name": "f2name",
            "last_name": "l2name",
            "password": "randompass",
            "national_code": "5566887799",
            "school_name": "schoolname",
            "lesson_name": "lessonname2",
        }

        self.client.post(self.register_url, self.user_data)
        self.client.post(self.register_url, self.user_data2)
        self.account1 = User.objects.get(username="user1")
        self.account2 = User.objects.get(username="user2")
        self.l1 = Lesson.objects.get(teacher=self.account1)
        self.l2 = Lesson.objects.get(teacher=self.account2)
        self.sample_news = News.objects.create(teacher=self.account1, body="..", title="...")

    def login_teacher_account(self):
        login_response = self.client.post(self.login_url,
                                          data={"username": self.user_data["username"],
                                                "password": self.user_data["password"]})
        self.assertEqual(200, login_response.status_code)
        token = login_response.data['token']
        token = 'Token ' + token
        header = {'HTTP_AUTHORIZATION': token}
        return header

    def test_user_cannot_register_with_no_data(self):
        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cannot_register_with_duplicate_data(self):
        self.client.post(self.register_url, self.user_data)
        res = self.client.post(self.register_url, self.user_data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_login(self):
        res = self.client.post(self.login_url,
                               data={"username": self.user_data["username"], "password": self.user_data["password"]})
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_teacher_can_add_student(self):
        header = self.login_teacher_account()
        res = self.client.put(
            reverse('lessons_detail', kwargs={'pk': self.l1.id}),
            data={"add_student_national_code": "1111111111"}, format='json', **header)
        student = User.objects.get(username="1111111111")
        lesson = Lesson.objects.get(id=self.l1.id)
        students = lesson.students.all()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(student in students)

    def test_teacher_cannot_add_student_in_others_lesson(self):
        header = self.login_teacher_account()
        res = self.client.get(
            reverse('lessons_detail', kwargs={'pk': self.l2.id}), **header)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_teacher_news(self):
        header = self.login_teacher_account()
        res = self.client.post(
            reverse('news_list_create'),
            data={"title": "t1", "body": "b1"}, format='json', **header)
        news = News.objects.filter(title="t1")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(news)

    def test_edit_profile(self):
        header = self.login_teacher_account()
        res = self.client.patch(
            reverse('profile', kwargs={'username': 'user1'}),
            data={"first_name": "changed"}, format='json', **header)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        user = User.objects.get(username='user1')
        self.assertEqual(user.first_name, "changed")

    def test_edit_news(self):
        header = self.login_teacher_account()
        res = self.client.patch(
            reverse('news_detail', kwargs={'pk': self.sample_news.id}),
            data={"title": "changed"}, format='json', **header)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        news = News.objects.get(id=self.sample_news.id)
        self.assertEqual(news.title, "changed")
