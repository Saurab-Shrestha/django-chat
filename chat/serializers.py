from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from chat.models import MessageModel
from rest_framework import serializers

User = get_user_model()

class MessageModelSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.email', read_only=True)
    recipient = serializers.CharField(source='recipient.email')

    def create(self, validated_data):
        user = self.context['request'].user
        recipient = get_object_or_404(
            User, email = validated_data['recipient']['email']
        )
        msg = MessageModel(user=user, recipient=recipient, body=validated_data['body'])
        msg.save()
        return msg
    
    class Meta:
        model = MessageModel
        fields = ('id', 'user', 'recipient', 'timestamp', 'body')
