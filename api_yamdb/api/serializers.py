from django.core import validators
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.fields import IntegerField

from reviews.models import Category, Comment, Genre, Review, Title, User


class ReviewSerialazer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate_score(self, value):
        if not (0 < value <= 10):
            raise serializers.ValidationError('Оценка должна быть от 0 до 10.')

    def validate(self, data):
        request = self.context['request']
        user = request.user
        title_id = request.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(
                title=title, author=user
            ).exists()
        ):
            raise ValueError('Вы можете оставить только один отзыв.')
        return data


class CommentSerialazer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
        read_only_fields = ('id', 'author', 'pub_date', 'review_id', )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        model = User

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать это имя.'
            )
        return data


class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254,
        validators=(validators.MaxLengthValidator(254),)
    )
    username = serializers.SlugField(
        max_length=150,
        validators=(
            validators.MaxLengthValidator(150),
            validators.RegexValidator(r'^[\w.@+-]+\Z')
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать это имя.'
            )
        return data


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        lookup_field = 'slug'
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id', )


class TitleReadSerializer(serializers.ModelSerializer):
    rating = IntegerField(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )
        model = Title


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'category',
            'genre',
        )


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        fields = ('username', 'confirmation_code',)
        model = User
