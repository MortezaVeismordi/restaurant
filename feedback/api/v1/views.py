from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from feedback.models import Feedback, FeedbackImage
from .serializers import FeedbackSerializer, FeedbackCreateSerializer, FeedbackImageSerializer

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['rating', 'customer']
    search_fields = ['comment', 'customer__username']
    ordering_fields = ['rating', 'created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return FeedbackCreateSerializer
        return FeedbackSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Feedback.objects.all()
        return Feedback.objects.filter(customer=user)

    @action(detail=True, methods=['patch'])
    def respond(self, request, pk=None):
        if not request.user.is_staff:
            return Response(
                {"error": "Only staff members can respond to feedback"},
                status=status.HTTP_403_FORBIDDEN
            )

        feedback = self.get_object()
        response = request.data.get('staff_response')
        
        if not response:
            return Response(
                {"error": "Staff response is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        feedback.staff_response = response
        feedback.save()
        serializer = self.get_serializer(feedback)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        recent_feedback = self.get_queryset().order_by('-created_at')[:5]
        serializer = self.get_serializer(recent_feedback, many=True)
        return Response(serializer.data)

class FeedbackImageViewSet(viewsets.ModelViewSet):
    queryset = FeedbackImage.objects.all()
    serializer_class = FeedbackImageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['feedback']
    ordering_fields = ['created_at'] 