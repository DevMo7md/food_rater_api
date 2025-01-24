from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid

# Create your models here.
class Meals(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def no_ratungs(self):
        no_ratings = Rate.objects.filter(meal=self).count()
        return no_ratings
    
    def avg_ratings(self):
        ratings = Rate.objects.filter(meal=self)
        sum_ratings = 0
        if self.no_ratungs() > 0:
            for i in ratings:
                sum_ratings += i.rating
            result = sum_ratings / self.no_ratungs()
            return round(result, 2)
        else:
            return 0

    def __str__(self):
        return self.name

class Rate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meals, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])

    def __str__(self):
        return f"{self.user.username} - {self.meal.name} - {self.rating}"

    class Meta:
        unique_together = ('user', 'meal')
