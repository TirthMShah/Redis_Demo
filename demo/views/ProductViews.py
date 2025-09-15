from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter, SearchFilter

from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache

from demo.models import Product
from demo.serializers import ProductSerializer

from demo.helper import generate_cache_key
import logging

logger = logging.getLogger(__name__)



class ProductListAPIView(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]

    filterset_fields = ['price']  # filter by price
    search_fields = ['name', 'description']  # search
    ordering_fields = ['price', 'created_at', 'name']  # order by
    ordering = ['-created_at']

    def list(self, request, *args, **kwargs):
        user = request.user.id if request.user.is_authenticated else "anonymous"
        cache_key = generate_cache_key(user, request.GET.urlencode(), 'products')

        try:
            cached_data = cache.get(cache_key)
            if cached_data:
                logger.info("⚡ From Redis Cache")
                return Response(cached_data)
        except Exception as e:
            logger.error(f"Redis cache get failed: {e}")

        logger.info("🐢 From DB")
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        try:
            cache.set(cache_key, serializer.data, timeout=300)     # cache for 5 minutes
            logger.info("✅ Data cached in Redis")
        except Exception as e:
            logger.error(f"Redis cache set failed: {e}")

        return Response(serializer.data)


class CreateProductAPIView(CreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def perform_create(self, serializer):
        product = serializer.save()
        cache.delete("products_list")  # clear cache when new product created
        return product
