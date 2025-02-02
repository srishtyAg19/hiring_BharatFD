from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.core.cache import cache
from .models import FAQ

class FAQModelTest(TestCase):
    """Test cases for FAQ model"""

    def setUp(self):
        """Create a sample FAQ object"""
        self.faq = FAQ.objects.create(question="Hello", answer="Test Answer")

    def test_translation_fields_exist(self):
        """Check if translation fields exist"""
        self.assertTrue(hasattr(self.faq, "question_hi"))  # Hindi translation field
        self.assertTrue(hasattr(self.faq, "question_bn"))  # Bengali translation field


class FAQAPITestCase(APITestCase):
    """Test cases for FAQ API"""

    def setUp(self):
        """Create some FAQ entries for testing"""
        self.faq1 = FAQ.objects.create(question="Hello", answer="Test Answer")
        self.faq2 = FAQ.objects.create(question="How are you?", answer="I'm fine.")
        cache.clear()  # Clear cache before running API tests

    def test_api_returns_faqs(self):
        """Test if API returns the list of FAQs"""
        url = reverse("faq-list")  # Use reverse to get URL dynamically
        response = self.client.get(url, {"lang": "en"})  # Call API with lang parameter
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Expecting 2 FAQs in response

    def test_api_returns_translated_faqs(self):
        """Test if API returns translated FAQs when language is provided"""
        url = reverse("faq-list")
        response = self.client.get(url, {"lang": "hi"})  # Test with Hindi language
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for faq in response.data:
            self.assertIn("question", faq)  # Ensure 'question' field exists in response

    def test_api_uses_cache(self):
        """Test if API caching works properly"""
        url = reverse("faq-list")
        cache.clear()  # Ensure cache is empty before test
        response1 = self.client.get(url, {"lang": "en"})
        response2 = self.client.get(url, {"lang": "en"})

        self.assertEqual(response1.data, response2.data)  # Cached response should be the same
