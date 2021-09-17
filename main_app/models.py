from django.db import models
from django.urls import reverse

# Create your models here.
# A tuple of 2-tuples
WATERINGS = (
    ('T', 'Top'),
    ('B', 'Bottom'),
)

class Plant(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    age = models.IntegerField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'plant_id': self.id})

# b - bottom water / t - top water
class Watering(models.Model):
    date = models.DateField('watering date')
    watering_type = models.CharField(
        max_length=1,
        choices=WATERINGS,
        default=WATERINGS[0][0]
)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_watering_type_display()} on {self.date}"
    class Meta:
        ordering = ['-date']
