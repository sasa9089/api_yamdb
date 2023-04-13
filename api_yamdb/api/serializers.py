from rest_framework import serializers

from django.shortcuts import get_object_or_404

from reviews.models import Review, Comment, User, Title, Category, Genre

import datetime as dt


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
                title=title, author = user
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


class EditSerializer(UserSerializer):
    role = serializers.CharField(read_only=True)


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email')
        model = User

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать это имя.'
            )
        return data


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre
    
    def validate(self, data):
        if self.context['request'].slug == data['slug']:
            raise serializers.ValidationError(
                'Поле slug жанра должно быть уникальным.'
            )
        return data


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    class Meta:
        fields = ('category', 'genre', 'name', 'year')
        model = Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category
    
