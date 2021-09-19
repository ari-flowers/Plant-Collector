from django.db import models
from django.urls import reverse
from datetime import date
# Create your models here.

WATERINGS = (
    ('T', 'Top'),
    ('B', 'Bottom'),
)

#inventory items model
class Item(models.Model):
    name = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('items_detail', kwargs={'pk': self.id})

#plant model
class Plant(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    age = models.IntegerField()
    items = models.ManyToManyField(Item)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'plant_id': self.id})
#====================================================================================
# ask for help here
    def watered_this_week(self):
        return self.watering_set.filter(date=date.today()).count() >= len(WATERINGS)

#====================================================================================
#watering model
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

#photo model
class Photo(models.Model):
    url = models.CharField(max_length=200)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for plant_id: {self.plant_id} @{self.url}"
