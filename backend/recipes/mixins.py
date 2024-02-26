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

    image = Base64ImageField(required=True, allow_null=True)

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None
