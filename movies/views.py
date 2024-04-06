from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination

from movies.permissions import IsEmployeeOrReadOnly
from movies.models import Movie
from movies.serializers import MovieSerializer


class MovieView(APIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsEmployeeOrReadOnly]

    def get(self, request: Request):
        movies = Movie.objects.all()
        result = self.paginate_queryset(movies, request, view=self)
        serializer = MovieSerializer(result, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request: Request):
        serializer = MovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status.HTTP_201_CREATED)


class MovieDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsEmployeeOrReadOnly]

    def get(self, request: Request, movie_id: int):
        found_movie = get_object_or_404(Movie, pk=movie_id)
        serializer = MovieSerializer(found_movie)
        return Response(
            serializer.data,
            status.HTTP_200_OK
        )

    def delete(self, request: Request, movie_id: int):
        found_movie = get_object_or_404(Movie, pk=movie_id)
        found_movie.delete()
        return Response(
           status=status.HTTP_204_NO_CONTENT
        )
