from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


class RegisterTestCase(APITestCase):
    def test_register(self):
        data = {
            'username': 'testcase',
            'email': 'testcase@example.com',
            'password1': 'password@123',
            'password2': 'password@123'
        }
        response = self.client.post(reverse('register'), data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
