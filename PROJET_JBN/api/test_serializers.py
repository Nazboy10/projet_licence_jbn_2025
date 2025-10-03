from django.test import TestCase
from api.serializers import UtilisateurSerializer
from SGCBA.models import Utilisateur


class UtilisateurSerializerTest(TestCase):
    def setUp(self):
        # Pas d'utilisateur créé ici pour éviter des duplicatas sur la DB de test
        pass

    def test_password_valid(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'role': 'secretaire',
            'password': 'Abcd1234!'
        }
        s = UtilisateurSerializer(data=data)
        self.assertTrue(s.is_valid(), s.errors)

    def test_password_too_short(self):
        data = {'username': 'u1', 'email': 'u1@example.com', 'role': 'secretaire', 'password': 'A1!a'}
        s = UtilisateurSerializer(data=data)
        self.assertFalse(s.is_valid())
        self.assertIn('password', s.errors)

    def test_password_missing_upper(self):
        data = {'username': 'u2', 'email': 'u2@example.com', 'role': 'secretaire', 'password': 'abcd1234!'}
        s = UtilisateurSerializer(data=data)
        self.assertFalse(s.is_valid())
        self.assertIn('password', s.errors)

    def test_password_missing_digit(self):
        data = {'username': 'u3', 'email': 'u3@example.com', 'role': 'secretaire', 'password': 'Abcdefgh!'}
        s = UtilisateurSerializer(data=data)
        self.assertFalse(s.is_valid())
        self.assertIn('password', s.errors)

    def test_password_missing_special(self):
        data = {'username': 'u4', 'email': 'u4@example.com', 'role': 'secretaire', 'password': 'Abcd12345'}
        s = UtilisateurSerializer(data=data)
        self.assertFalse(s.is_valid())
        self.assertIn('password', s.errors)
