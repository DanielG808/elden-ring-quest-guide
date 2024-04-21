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
    items_rewarded = models.ManyToManyField(Item, related_name="items_rewarded")


class CustomUser(AbstractUser):
    quest_steps_progress = models.ManyToManyField(QuestStep, through='UserStepProgress')
    quests_in_proress = models.ManyToManyField(Quest, through='UserQuestProgress')
    quests_completed = models.ManyToManyField(Quest, through='UserQuestProgress')
    bosses_defeated = models.ManyToManyField(Boss, through='UserBossDefeated')


class UserStepProgress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quest_step = models.ForeignKey(QuestStep, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)


class UserQuestProgress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)
    in_progress = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)


class UserBossDefeated(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    boss = models.ForeignKey(Boss, on_delete=models.CASCADE)
    defeated = models.BooleanField(default=False)
    # Perhaps we add an 'attempts' field if we wanna track that later?

    


