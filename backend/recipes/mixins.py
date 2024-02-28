import base64

from django.core.files.base import ContentFile
from rest_framework.serializers import ImageField


class Base64ImageField(ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class GetImageMixin:
    """Миксин для метода получения картинки."""

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None


class IsFavoritedMixin:
    """Миксин для метода определения избранного."""

    def get_is_favorited(self, obj):
        return (
            False if self.context.get('request').user.is_anonymous
            else obj in self.context.get('request').user.favorite_recipes.all()
        )


class isInShoppingCartMixin:
    """Миксин для метода определения назождения в списке покупок."""

    def get_is_in_shopping_cart(self, obj):
        return (
            False if self.context.get('request').user.is_anonymous
            else obj in self.context.get('request').user.shopping_list.all()
        )
