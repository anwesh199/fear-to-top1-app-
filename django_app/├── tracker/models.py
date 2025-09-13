from django.db import models
from django.contrib.auth.models import User

class Domain(models.Model):
    name = models.CharField(max_length=100, unique=True)
    weight = models.FloatField(default=0.2)

    def __str__(self):
        return self.name

class Task(models.Model):
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name="tasks")
    name = models.CharField(max_length=100)
    xp = models.IntegerField(default=0)
    streak = models.IntegerField(default=0)
    goal_min = models.IntegerField(default=30)
    difficulty = models.FloatField(default=2.0)
    locked = models.BooleanField(default=False)
    last_done = models.DateField(null=True, blank=True)

    def level(self):
        if self.xp < 100: return "Beginner"
        if self.xp < 300: return "Intermediate"
        if self.xp < 700: return "Pro"
        return "Top 1%"

    def __str__(self):
        return f"{self.domain} → {self.name}"

class Log(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="logs")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    minutes = models.IntegerField()
    xp_gain = models.IntegerField()
    note = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
