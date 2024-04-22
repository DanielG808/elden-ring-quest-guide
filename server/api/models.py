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
    steps = models.ManyToManyField(QuestStep, related_name='quest_steps')
    bosses = models.ManyToManyField(Boss, related_name="bosses")
    items_required = models.ManyToManyField(Item, related_name="items_required")
    items_rewarded = models.ManyToManyField(Item, related_name="items_rewarded")


class CustomUser(AbstractUser):
    quest_steps_progress = models.ManyToManyField(QuestStep, through='UserStepProgress', related_name='quest_steps_progress')
    quests_in_progress = models.ManyToManyField(Quest, through='UserQuestProgress', related_name='quests_in_progress')
    quests_completed = models.ManyToManyField(Quest, through='UserQuestCompleted', related_name='quests_completed')
    bosses_defeated = models.ManyToManyField(Boss, through='UserBossDefeated', related_name='bosses_defeated')


class UserStepProgress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quest_step = models.ForeignKey(QuestStep, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)


class UserQuestProgress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)
    in_progress = models.BooleanField(default=False)
    

class UserQuestCompleted(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

class UserBossDefeated(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    boss = models.ForeignKey(Boss, on_delete=models.CASCADE)
    defeated = models.BooleanField(default=False)
    # Perhaps we add an 'attempts' field if we wanna track that later?

    


