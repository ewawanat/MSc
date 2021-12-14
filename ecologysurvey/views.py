from django.shortcuts import render
from enterdata.models import Category
from django.contrib.auth.decorators import login_required


# method to display all categories of species existing in database on the homepage:
def homePage(request):
    categories = Category.objects.all()
    context_dict = {}
    context_dict['categories'] = []
    for category in categories: 
        context_dict['categories'].append(category)
    display = True
    context_dict['display'] = display
    # print(context_dict['categories'])
    return render(request, 'homepage.html', context = context_dict)


# set the chosen category to be empty
chosen_category = ''
#method to go to the page for the chosen category:
@login_required(login_url="/accounts/login/") #this is so that the user can only add data if they are logged in, if not logged in, redirect to login page
def categoryChoice(request, category_name_slug): 
    global chosen_category
    chosen_category = category_name_slug #chosen category becomes the name of the category chosen by user (e.g. bird, insect, etc)
    # print('chosen_category')
    # print(chosen_category)
    # print(category_name_slug)
    return render(request, 'category.html')