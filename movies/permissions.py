
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.views import APIView

from movies.models import Movie


class IsEmployeeOrReadOnly(BasePermission):
    def has_permission(self, request, view: APIView):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_superuser
        )


class IsMovieOwner(BasePermission):
    def has_object_permission(self, request, view: APIView, obj: Movie):
        return obj == request.user or request.user.is_superuser
