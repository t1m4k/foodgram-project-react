from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import exceptions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from recipes.models import (FavoriteRecipe, Ingredient, IngredientsRecipe,
                            Recipe, ShoppingCart, Subscription, Tag)

from .filters import IngredientFilter, RecipeFilter
from .permissions import IsAuthorOrAdminPermission
from .serializers import (IngredientSerializer, LightRecipeSerializer,
                          RecipeCreateUpdateSerializer, RecipeSerializer,
                          SubscriptionSerializer, TagSerializer)

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @action(
        methods=('get',),
        detail=False,
        permission_classes=(IsAuthenticated,),
        serializer_class=SubscriptionSerializer
    )
    def subscriptions(self, request):
        user = self.request.user
        user_subsriptions = user.follower.all()
        authors = [item.following.id for item in user_subsriptions]
        queryset = User.objects.filter(pk__in=authors)
        pages = self.paginate_queryset(queryset)
        serializer = self.get_serializer(pages, many=True)
        return self.get_paginated_response(serializer.data)

    @action(
        methods=('post', 'delete'),
        detail=True,
        serializer_class=SubscriptionSerializer
    )
    def subscribe(self, request, id=None):
        user = self.request.user
        author = get_object_or_404(User, pk=id)
        if self.request.method == 'POST':
            if user == author:
                raise exceptions.ValidationError(
                    'Нельзя подписываться на самого себя'
                )
            if Subscription.objects.filter(user=user,
                                           following=author).exists():
                raise exceptions.ValidationError('Подписка уже оформлена')
            Subscription.objects.create(user=user, following=author)
            serializer = self.get_serializer(author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if self.request.method == 'DELETE':
            if not Subscription.objects.filter(user=user,
                                               following=author).exists():
                raise exceptions.ValidationError(
                    'Подписка уже удалена'
                )
            subscription = get_object_or_404(Subscription,
                                             user=user,
                                             following=author)
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrAdminPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return RecipeCreateUpdateSerializer
        return RecipeSerializer

    @action(
        methods=('post', 'delete'),
        detail=True,
    )
    def favorite(self, request, pk):
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if self.request.method == 'POST':
            if FavoriteRecipe.objects.filter(
                user=user, recipe__id=pk
            ).exists():
                raise exceptions.ValidationError('Рецепт уже добавлен')
            FavoriteRecipe.objects.create(user=user, recipe=recipe)
            serializer = LightRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if self.request.method == 'DELETE':
            if not FavoriteRecipe.objects.filter(user=user,
                                                 recipe__id=pk).exists():
                raise exceptions.ValidationError(
                    'Рецепт уже удален'
                )
            favorite = get_object_or_404(FavoriteRecipe,
                                         user=user,
                                         id=pk)
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(
        methods=('post', 'delete'),
        detail=True,
    )
    def shopping_cart(self, request, pk):
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if self.request.method == 'POST':
            if ShoppingCart.objects.filter(user=user, recipe__id=pk).exists():
                raise exceptions.ValidationError(
                    'Рецепт уже добавлен'
                )
            ShoppingCart.objects.create(user=user, recipe=recipe)
            serializer = LightRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if self.request.method == 'DELETE':
            if not ShoppingCart.objects.filter(user=user,
                                               recipe__id=pk).exists():
                raise exceptions.ValidationError('Рецепт уже удален')
            shopping_cart = get_object_or_404(ShoppingCart,
                                              user=user,
                                              id=pk)
            shopping_cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(
        methods=('get',),
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        user = request.user
        if not user.shopping.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        ingredients = IngredientsRecipe.objects.filter(
            recipe__shopping__user=request.user
        ).values('ingredient__name', 'ingredient__measurement_unit'
                 ).annotate(amount=Sum('amount'))
        shopping_list = 'Список покупок:\n\n'
        shopping_list += '\n'.join([
            f'{ingredient["ingredient__name"]} '
            f'{ingredient["ingredient__measurement_unit"]} '
            f'-- {ingredient["amount"]}'
            for ingredient in ingredients
        ])
        response = HttpResponse(shopping_list, content_type='text.txt')
        response['Content-Disposition'] = (
            'attachment; filename = shopping_list.txt'
        )
        return response
