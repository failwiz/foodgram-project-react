from rest_framework.permissions import BasePermission, SAFE_METHODS


class AnonymousReadOnly(BasePermission):
    """Класс для проверки анонимного доступа только для чтения."""

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """Класс для проверки прав на редактирование объекта."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user
