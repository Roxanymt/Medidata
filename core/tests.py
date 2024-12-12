from django.test import TestCase
from django.urls import reverse

# Create your tests here.
class SQLInjectionTest(TestCase):
    def test_sql_injection(self):
        # Realiza una solicitud GET con un intento de inyección SQL
        response = self.client.get(reverse('login') + "?q=' OR '1'='1")
        # Verifica que la respuesta no contenga un resultado inesperado
        self.assertNotContains(response, "unexpected result")

class XSSTest(TestCase):
    def test_xss_protection(self):
        # Realiza una solicitud POST con un intento de XSS
        response = self.client.post(reverse('login'), {'comment': '<script>alert("XSS")</script>'})
        # Verifica que la respuesta no contenga el script
        self.assertNotContains(response, '<script>alert("XSS")</script>')