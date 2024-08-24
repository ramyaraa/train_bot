from django.db import models


class Course(models.Model):
    CATEGORY_CHOICES = [
        ('python', 'Python'),
        ('java', 'Java'),
        ('javascript', 'JavaScript'),
        ('webdev', 'Web Development'),
        ('machinelearning', 'Machine Learning'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    url = models.URLField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')

    def __str__(self):
        return self.title

class UserData(models.Model):
    id = models.BigIntegerField(primary_key=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)  # Allow null or blank values
    username = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} - {self.last_name}"
