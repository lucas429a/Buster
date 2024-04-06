from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import UserSerializers
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from movies.permissions import IsMovieOwner
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from users.models import User


class UserView(APIView):
    def post(self, request: Request):
        serializer = UserSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class UserDetailView(APIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsMovieOwner, IsAuthenticated]

    def get(self, request: Request, user_id: int):
        try:
            found_user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "Not found."}, status.HTTP_404_NOT_FOUND
            )
        self.check_object_permissions(request, found_user)
        serializer = UserSerializers(found_user)
        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request: Request, user_id: int):
        user = get_object_or_404(User, pk=user_id)
        self.check_object_permissions(request, user)
        serializer = UserSerializers(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)
