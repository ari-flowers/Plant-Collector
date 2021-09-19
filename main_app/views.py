from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Plant, Item, Photo
from .forms import WateringForm
import uuid
import boto3
import botocore
import os

def add_photo(request, plant_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # we can assign to plant_id or plant (if you have a plant object)
            Photo.objects.create(url=url, plant_id=plant_id)
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', plant_id=plant_id)


def plants_detail(request, plant_id):
    plant = Plant.objects.get(id=plant_id)
    #items the plant does not currently have equipped
    items_plant_doesnt_have = Item.objects.exclude(id__in = plant.items.all().values_list('id'))

    watering_form = WateringForm()
    return render(request, 'plants/detail.html', {
        'plant': plant, 'watering_form': watering_form,
        'items': items_plant_doesnt_have
    })

def add_watering(request, plant_id):
  # create a ModelForm instance using the data in request.POST
  form = WateringForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it
    # has the plant_id assigned
    new_watering = form.save(commit=False)
    new_watering.plant_id = plant_id
    new_watering.save()
  return redirect('detail', plant_id=plant_id)

def plants_index(request):
  plants = Plant.objects.all()
  return render(request, 'plants/index.html', { 'plants': plants })

# Define the home view
def home(request):
  return render(request, 'home.html')

# Define about view
def about(request):
    return render(request, 'about.html')

class PlantCreate(CreateView):
  model = Plant
  fields = ['name', 'species', 'description', 'age']
  # success_url = '/plants'

class PlantUpdate(UpdateView):
  model = Plant
  fields = ['species', 'description', 'age']

class PlantDelete(DeleteView):
  model = Plant
  success_url = '/plants/'

#Item views
class ItemList(ListView):
    model = Item

class ItemDetail(DetailView):
    model = Item

class ItemCreate(CreateView):
    model = Item
    fields = '__all__'

class ItemUpdate(UpdateView):
    model = Item
    fields = ['name', 'size', 'description']

class ItemDelete(DeleteView):
    model = Item
    success_url = '/items'

#items / plants many to many association
def assoc_item(request, plant_id, item_id):
  Plant.objects.get(id=plant_id).items.add(item_id)
  return redirect('detail', plant_id=plant_id)
