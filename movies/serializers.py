from rest_framework import serializers
from movies.models import Rating_choices
from movies.models import Movie


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True),
    title = serializers.CharField(max_length=127),
    duration = serializers.CharField(max_length=10, required=False)
    rating = serializers.ChoiceField(
        choices=Rating_choices.choices,
        default=Rating_choices.G
    )
    synopsis = serializers.CharField(required=False)
    added_by = serializers.SerializerMethodField()

    def get_added_by(self, movie: Movie):
        return movie.user.email

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)
