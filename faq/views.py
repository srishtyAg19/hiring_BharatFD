from rest_framework import generics
from rest_framework.response import Response
from django.core.cache import cache
from .models import FAQ
from .serializers import FAQSerializer


class FAQListView(generics.ListAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer




def list(self, request, *args, **kwargs):
        lang = request.GET.get('lang', 'en')  # Get the language parameter (default is 'en')
        cache_key = f'faqs_{lang}'  # Use language as part of the cache key
        cached_data = cache.get(cache_key)  # Try to get data from cache

        if cached_data:
            # If data is found in cache, return it
            return Response(cached_data)

        queryset = self.get_queryset()  # Get all FAQs
        for faq in queryset:
            # Get the translated question based on the language
            faq.question = faq.get_translated_question(lang)

        # Serialize the data
        serializer = self.get_serializer(queryset, many=True)
        
        # Set the cache for 1 hour (3600 seconds)
        cache.set(cache_key, serializer.data, timeout=3600)
        return Response(serializer.data)
