from django.core import validators
from rest_framework import serializers
from rest_framework.fields import IntegerField
from reviews.models import Category, Comment, Genre, Review, Title, User


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
        read_only_fields = ("title", "author")

    def validate(self, data):
        request = self.context['request']
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')
        if not request.method == 'POST':
            return data
        if Review.objects.filter(author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'Вы можете оставить только один отзыв.'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
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
    )
    username = serializers.CharField(
        max_length=150,
        validators=(
            validators.RegexValidator(r'^[\w.@+-]+\Z'),
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                {'username': ['Нельзя использовать это имя.']}
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

    def to_representation(self, title):
        return TitleReadSerializer(title).data

    def create(self, validateddata):
        genre = validateddata.pop('genre', [])
        if not genre:
            raise serializers.ValidationError(
                {'genre': ['Список жанров не может быть пустым']})
        title = Title.objects.create(**validateddata)
        title.genre.set(genre)
        return title


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=(
            validators.RegexValidator(r'^[\w.@+-]+\Z'),
        )
    )
    confirmation_code = serializers.CharField()

    class Meta:
        fields = ('username', 'confirmation_code',)
        model = User

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать это имя.'
            )
        return data
