from django.shortcuts import render
from .models import Plant

# Add the plant class & list and view function below the imports
# class Plant:  # Note that parens are optional if not inheriting from another class
#   def __init__(self, name, species, description, age):
#     self.name = name
#     self.species = species
#     self.description = description
#     self.age = age
#
# plants = [
#   Plant('Epipremnum Pinatum Variegata', 'Pothos', 'Grown from a node.', 0),
#   Plant('Pink Princess', 'Philodendron', '3 inch PPP', 1),
#   Plant('Pink Splash', 'Syngonium', 'Top 5 faves', 1)
# ]
def plants_index(request):
  plants = Plant.objects.all()
  return render(request, 'plants/index.html', { 'plants': plants })

# Define the home view
def home(request):
  return render(request, 'home.html')

# Define about view
def about(request):
    return render(request, 'about.html')
