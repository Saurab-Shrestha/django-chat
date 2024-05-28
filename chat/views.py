from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication

from drf_spectacular.utils import extend_schema

from django_chat import settings
from chat.models import MessageModel
from chat.serializers import MessageModelSerializer

User = get_user_model()

class MessagePagination(PageNumberPagination):
    """
    Custom pagination class for setting page size and maximum page size.
    """
    page_size = settings.MESSAGES_TO_LOAD

@extend_schema(tags=["Messages"], description="ModelViewset for CRUD operations with custom Listing and Retrieving messages.")
class MessageModelViewSet(ModelViewSet):
    queryset = MessageModel.objects.all()
    serializer_class = MessageModelSerializer
    allowed_methods = ('GET', 'POST', 'HEAD', 'OPTIONS')
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    pagination_class = MessagePagination    

    @extend_schema(
        summary="List Messages",
        description="List messages for the authenticated user. Optionally filter by target email.",
        responses=MessageModelSerializer(many=True)
    )
    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(Q(recipient=request.user) |
                                             Q(user=request.user))
        target = self.request.query_params.get('target', None)
        if target is not None:
            self.queryset = self.queryset.filter(
                Q(recipient=request.user, user__email=target) |
                Q(recipient__email=target, user=request.user))
        return super(MessageModelViewSet, self).list(request, *args, **kwargs)


    @extend_schema(
        summary="Retrieve Message",
        description="Retrieve a specific message by pk or email for the authenticated user.",
        responses=MessageModelSerializer
    )
    def retrieve(self, request, *args, **kwargs):
        msg = get_object_or_404(
            self.queryset.filter(Q(recipient=request.user) |
                                 Q(user=request.user),
                                 Q(pk=kwargs['pk'])))
        serializer = self.get_serializer(msg)
        return Response(serializer.data)
    