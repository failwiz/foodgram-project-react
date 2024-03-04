import base64

from django.core.files.base import ContentFile
from rest_framework.serializers import ImageField


class Base64ImageField(ImageField):
    """Поле сериализатора для сохранения картинки из строки Base64."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class GetImageMixin:
    """Миксин для метода получения картинки."""

    def get_image_url(self, obj):
        return obj.image.url if obj.image else None


class IsFavoritedMixin:
    """Миксин для метода определения избранного."""

    def get_is_favorited(self, obj):
        return (
            obj in self.context.get('request').user.favorite_recipes.all()
            if (
                self.context.get('request')
                and self.context.get('request').user.is_authenticated
            ) else False
        )


class isInShoppingCartMixin:
    """Миксин для метода определения назождения в списке покупок."""

    def get_is_in_shopping_cart(self, obj):
        return (
            obj in self.context.get('request').user.shopping_list.all()
            if (
                self.context.get('request')
                and self.context.get('request').user.is_authenticated
            ) else False
        )
