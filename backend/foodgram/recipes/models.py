from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from colorfield.fields import ColorField

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    color = ColorField(format='hex', default='#FF0000', unique=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    measurement_unit = models.CharField(max_length=15)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='recipes'
    )
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='recipes/')
    text = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredient, through='IngredientsRecipe'
    )
    tags = models.ManyToManyField(
        Tag, verbose_name='tags'
    )
    cooking_time = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MinValueValidator(1,
                              message='Минимальное значение 1')
        ]
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)

    def is_favorited(self, user):
        return self.favorites.filter(user=user).exists()

    def is_in_shopping_cart(self, user):
        return self.shopping.filter(user=user).exists()

    def __str__(self):
        return self.name


class IngredientsRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MinValueValidator(1,
                              message='Минимальное значение 1')
        ]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_reciepe_ingredient'
            ),
        ]


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='favorites'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='favorites'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_user_recipe'
            ),
        ]


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shopping'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='shopping'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_user_recipes'
            ),
        ]


class Subscription(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower',
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following',
    )

    def __str__(self):
        return self.user.username

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_author_user_following',
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('following')),
                name='self_follower'
            ),
        ]
