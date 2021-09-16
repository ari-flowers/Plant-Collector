from django.shortcuts import render

# Add the plant class & list and view function below the imports
class Plant:  # Note that parens are optional if not inheriting from another class
  def __init__(self, name, breed, description, age):
    self.name = name
    self.breed = breed
    self.description = description
    self.age = age

plants = [
  Plant('Lolo', 'tabby', 'foul little demon', 3),
  Plant('Sachi', 'tortoise shell', 'diluted tortoise shell', 0),
  Plant('Raven', 'black tripod', '3 legged plant', 4)
]

# Define the home view
def home(request):
  return render(request, 'home.html')

# Define about view
def about(request):
    return render(request, 'about.html')

# Define index view
def plants_index(request):
    return render(request, 'plants/index.html', { 'plants': plants })
