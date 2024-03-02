from re import match

from django.core.exceptions import ValidationError


class PatternValidator:
    """Валидатор на соответствие шаблону."""

    def __init__(self, pattern) -> None:
        self.pattern = pattern

    def __call__(self, value):
        if not match(self.pattern, value):
            raise ValidationError('Поле содержит недопустимые символы')
        return value
