from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET

from recipes.forms import RecipeForm
from recipes.models import Recipe


def index(request):
    recipes = Recipe.objects.all().order_by('time')
    context = {
        'recipes':recipes,
    }
    return render(request,'index.html',context)


def create(request):
    if request.method == "GET":
        form = RecipeForm()
        context = {
            'form':form
        }
        return render(request, 'create.html',context)
    else:
        recipes = Recipe.objects.all()
        form = RecipeForm(request.POST)
        context = {
            'recipes': recipes,
            'form': form,
        }
        if form.is_valid():
            form.save()
            return render(request, 'index.html',context)
        else:
            return render(request, 'create.html',context)


def edit(request,pk):
    recipe = Recipe.objects.get(pk=pk)
    if request.method == "GET":
        form = RecipeForm(instance=recipe)
        context = {
            "form": form,
            'pk': pk
        }
        return render(request, 'edit.html',context)
    else:
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            context = {
                'form': form,
                'pk': pk
            }
            return render(request,'edit.html',context)


def delete(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    recipe.delete()
    return redirect('index')

@require_GET
def details(request,pk):
    recipe = Recipe.objects.get(pk=pk)
    context = {
        'recipe': recipe,
        'pk': pk
    }
    return render(request, 'details.html', context)
