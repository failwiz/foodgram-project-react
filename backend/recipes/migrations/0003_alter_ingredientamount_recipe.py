# Generated by Django 4.2 on 2024-02-20 10:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_tag_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientamount',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_amounts', to='recipes.recipe', verbose_name='Рецепт'),
        ),
    ]
