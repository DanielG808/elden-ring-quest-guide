from django.db import models
from django.contrib.auth.models import AbstractUser


class Item(models.Model):
    name = models.CharField(max_length=100)


class Boss(models.Model):
    name = models.CharField(max_length=100)


class QuestStep(models.Model):
    step = models.CharField(max_length=500)


class Quest(models.Model):
    title = models.CharField(max_length=200)
    steps = models.ManyToManyField(QuestStep, on_delete=models.CASCADE, related_name='quest_steps')
    bosses = models.ManyToManyField(Boss, related_name="bosses")
    items_required = models.ManyToManyField(Item, related_name="items_required")
    items_rewarded = models.ManyToManyField(Item, related_name="items_rewared")

    


