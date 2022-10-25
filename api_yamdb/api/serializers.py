from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from reviews.models import Category, Genre, Title, Review, Comment


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели User."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        required_fields = ('username', 'email')

    def validate_username(self, value):
        invalid_username = 'me'
        if value == invalid_username:
            raise serializers.ValidationError('Недопустимый username')
        return value

    def validate(self, data):
        request = self.context.get("request")
        user = request.user
        if (request.method == 'PATCH' and not user.is_admin):
            data['role'] = user.role
        return data


class ReviewSerializer(serializers.ModelSerializer):
    """Сериалайзер модели Review"""
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        """Проверка на уникальность отзыва юзер-произведение при публикации"""
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError('Вы не можете добавить более'
                                      'одного отзыва на произведение')
        return data

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """Сериалайзер модели Comment"""
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер модели Category"""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериалайзер модели Genre"""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleListSerializer(serializers.ModelSerializer):
    """Сериалайзер модели Title для просмотра"""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)

    class Meta:
        model = Title
        fields = ('id',
                  'name',
                  'year',
                  'rating',
                  'description',
                  'genre',
                  'category')
        required_fields = ('name',)


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class AuthUserSerializer(serializers.ModelSerializer):
    """Сериалайзер для процедуры регистрации."""
    confirmation_code = serializers.HiddenField(default='')

    class Meta:
        model = User
        fields = (
            'username', 'email', 'confirmation_code'
        )
        required_fields = ('username', 'email')

    def validate_username(self, value):
        invalid_username = 'me'
        if value == invalid_username:
            raise serializers.ValidationError('Недопустимый username')
        return value


class TokenSerializer(serializers.Serializer):
    """Сериалайзер для выдачи токена."""
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)
