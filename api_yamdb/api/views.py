from django.db import IntegrityError
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken

from .permissions import IsAuthorOrModeratorOrAdminOrReadOnly, IsAdminOrReadOnly, IsAuthorizedOrAdminOrSuperuser
from .serializers import ReviewSerialazer, CommentSerialazer, UserSerializer, CreateUserSerializer, TitleSerializer, CategorySerializer, GenreSerializer, TokenSerializer 
from reviews.models import Title, User, Genre, Category



class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerialazer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorOrModeratorOrAdminOrReadOnly,
    )

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()
    
    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerialazer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorOrModeratorOrAdminOrReadOnly
    )

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        review = get_object_or_404(
            title.reviews, pk=self.kwargs.get('review_id')
        )
        return review.comments.all()
    
    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        review = get_object_or_404(
            title.reviews, pk=self.kwargs.get('review_id')
        )
        serializer.save(author=self.request.user, review=review)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthorizedOrAdminOrSuperuser,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=(['GET', 'PATCH']),
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated,),
    )
    def users(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data)


@api_view(['POST'])
def create_user(request):
    serializer = CreateUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']
    try:
        user, created = User.objects.get_or_create(
            username=username, email=email
        )
    except IntegrityError as error:
        raise ValidationError(f'{error}')
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Регистрация на сайте YaMDb',
        message=f'Проверочный код: {confirmation_code}',
        from_email='admin@yamdb.com',
        recipient_list=[user.email],
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User, username=serializer.validated_data.get('username')
    )
    if default_token_generator.check_token(
            user, serializer.validated_data.get("confirmation_code")
    ):
        token = AccessToken.for_user(user)
        return Response(
            {'token': f'{token}'}, status=status.HTTP_200_OK
        )
    return Response(
        serializer.errors, status=status.HTTP_400_BAD_REQUEST
    )


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
