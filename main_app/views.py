from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Plant, Item, Photo
from .forms import WateringForm
import uuid
import boto3
import botocore
import os

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

@login_required
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

@login_required
def plants_detail(request, plant_id):
    plant = Plant.objects.get(id=plant_id)
    #items the plant does not currently have equipped
    items_plant_doesnt_have = Item.objects.exclude(id__in = plant.items.all().values_list('id'))

    watering_form = WateringForm()
    return render(request, 'plants/detail.html', {
        'plant': plant, 'watering_form': watering_form,
        'items': items_plant_doesnt_have
    })

@login_required
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

@login_required
def plants_index(request):
  plants = Plant.objects.filter(user=request.user)
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
  def form_valid(self, form):
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user
    return super().form_valid(form)

class PlantUpdate(LoginRequiredMixin, UpdateView):
  model = Plant
  fields = ['species', 'description', 'age']

class PlantDelete(LoginRequiredMixin, DeleteView):
  model = Plant
  success_url = '/plants/'

#Item views
class ItemList(LoginRequiredMixin, ListView):
    model = Item

class ItemDetail(LoginRequiredMixin, DetailView):
    model = Item

class ItemCreate(LoginRequiredMixin, CreateView):
    model = Item
    fields = '__all__'

class ItemUpdate(LoginRequiredMixin, UpdateView):
    model = Item
    fields = ['name', 'size', 'description']

class ItemDelete(LoginRequiredMixin, DeleteView):
    model = Item
    success_url = '/items'

#items / plants many to many association
@login_required
def assoc_item(request, plant_id, item_id):
    Plant.objects.get(id=plant_id).items.add(item_id)
    return redirect('detail', plant_id=plant_id)

def unassoc_item(request, plant_id, item_id):
    Plant.objects.get(id=plant_id).items.remove(item_id)
    return redirect('detail', plant_id=plant_id)
