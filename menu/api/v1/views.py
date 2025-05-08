from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from menu.models import Category, MenuItem
from .serializers import CategorySerializer, MenuItemSerializer, MenuItemDetailSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    filterset_fields = ['category', 'is_available']
    search_fields = ['name', 'description', 'ingredients']
    ordering_fields = ['price', 'name', 'created_at']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MenuItemDetailSerializer
        return MenuItemSerializer

    @action(detail=False, methods=['get'])
    def available(self, request):
        available_items = self.queryset.filter(is_available=True)
        serializer = self.get_serializer(available_items, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_category(self, request):
        category_slug = request.query_params.get('category', None)
        if category_slug:
            items = self.queryset.filter(category__slug=category_slug)
            serializer = self.get_serializer(items, many=True)
            return Response(serializer.data)
        return Response({"error": "Category slug is required"}, status=400) 