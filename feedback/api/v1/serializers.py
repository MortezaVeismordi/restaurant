from rest_framework import serializers
from feedback.models import Feedback, FeedbackImage

class FeedbackImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackImage
        fields = ['id', 'image', 'created_at']
        read_only_fields = ['created_at']

class FeedbackSerializer(serializers.ModelSerializer):
    images = FeedbackImageSerializer(many=True, read_only=True)
    customer_name = serializers.CharField(source='customer.username', read_only=True)
    order_details = serializers.SerializerMethodField()

    class Meta:
        model = Feedback
        fields = [
            'id', 'customer', 'customer_name', 'order', 'order_details',
            'rating', 'comment', 'staff_response', 'images',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'staff_response']

    def get_order_details(self, obj):
        if obj.order:
            return {
                'id': obj.order.id,
                'total_price': obj.order.total_price,
                'status': obj.order.status
            }
        return None

class FeedbackCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        required=False
    )

    class Meta:
        model = Feedback
        fields = ['customer', 'order', 'rating', 'comment', 'images']

    def create(self, validated_data):
        images = validated_data.pop('images', [])
        feedback = Feedback.objects.create(**validated_data)
        
        for image in images:
            FeedbackImage.objects.create(feedback=feedback, image=image)
        
        return feedback 