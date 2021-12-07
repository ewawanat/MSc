from django.forms.widgets import Select
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from enterdata.models import Country, County, Sighting, Species, Category
from . import forms
import json
from django.http.response import HttpResponse, JsonResponse
import csv
import ecologysurvey.views 

# @login_required(login_url="/accounts/login/") #this is so that the user can only add data if they are logged in, if not logged in, redirect to login page
# def categoryChoice(request, category_name_slug): 
#     print(category_name_slug)
#     return render(request, 'category.html')
 
@login_required(login_url="/accounts/login/") #this is so that the user can only add data if they are logged in, if not logged in, redirect to login page
def displayData(request):
    # global chosen_category
    # print(chosen_category)
    chosen_category = ecologysurvey.views.chosen_category
    context_dict = {}
    category = {'name': chosen_category}
    display_form = forms.DisplayData(category)
    context_dict['form'] = display_form

    # if request.method == 'POST': 
        # print("request.POST:")
        # print(request.POST)
        # print("!!!! species_name printed:")
        # print(request.POST['species_name'])
        # print("getlist")
        # print(request.POST.getlist('species_name'))

        # print(request.POST.getlist('species_name')[0])
    

        # selected_species = request.POST.getlist('species_name')
        # from_date_selected = request.POST['from_date']
        # to_date_selected = request.POST['to_date']

        # list_dict = [  
        # ] #make an array 

            
        # for each_species in selected_species:       # iterate over selected species
        #     result = Species.objects.get(id=each_species) # match the id with each of the species id
        #     all_sightings = Sighting.objects.filter(species = result) \
        #         .filter(in_country__in = request.POST.getlist('in_country')) \
        #         .filter(in_county__in = request.POST.getlist('in_county')) \
        #         .filter(date_seen__range = [from_date_selected, to_date_selected])
        #     # create an all_sightings varable which is filtered by the searched for data

        #     # print(all_sightings)

        
        #     for i in all_sightings: # looop over all the sightings 
        #         occurrence = 0 #start counting ocurrence of each sighting at 0
        #         for j in all_sightings: 
        #             if i.species.name == j.species.name: #when the same species name is found
        #                 occurrence += 1 #add 1 to the occurrence 
                        
        #         dict = {'species_name': i.species.name, 'frequency': occurrence}  #create a dict with all species names and frequency of their occurrence       
        #         name_exists = False # set the name existing in the dictionary to false
        #         for name in list_dict: # loop over the names in the dictionary
        #             if len(list_dict)!=0: # if the length of the dictionary is not 0
        #                 if name["species_name"] == i.species.name: #if the name of the species is equal to the one currently being looked at 
        #                     name_exists = True #set name_exists to true (name exists in the dictionary)
        #         if name_exists == False: #if name does not exist in the dictionary 
        #             list_dict.append(dict) #append the name as a key to the dict


        # # print(list_dict)
        # print("line graph data:")

        # all_birds_sighted_json = json.dumps(list_dict) 
        # context_dict['jsondata'] = all_birds_sighted_json
        # # print(all_birds_sighted_json)
    return render(request, 'displaydata/displaydata.html', context = context_dict)

#AJAX Species.objects.get(id=each_species)
def load_counties(request):
    # print("we are here!")
    # print(request.GET)
    country_id = request.GET.getlist('country_id[]')
    # print(country_id) 

    counties = County.objects.filter(in_country_id__in=country_id).all()
    # print(counties)
    
    return JsonResponse(list(counties.values('in_country', 'name')), safe=False)


@csrf_exempt
def create_bargraph(request):
    print("We are HEREEEEEEEEE")
    print(request.POST)
    selected_species = request.POST.getlist('species[]')
    from_date_selected = request.POST['from_date']
    to_date_selected = request.POST['to_date']

    print(selected_species)
    print(from_date_selected)
    print(to_date_selected)

    list_dict = [  
    ] #make an array 

            
    for each_species in selected_species:       # iterate over selected species
        result = Species.objects.get(id=each_species) # match the id with each of the species id
        all_sightings = Sighting.objects.filter(species = result) \
           .filter(in_country__in = request.POST.getlist('country[]')) \
            .filter(in_county__in = request.POST.getlist('county[]')) \
            .filter(date_seen__range = [from_date_selected, to_date_selected])
            # create an all_sightings varable which is filtered by the searched for data

        print(all_sightings)

        
        for i in all_sightings: # looop over all the sightings 
            occurrence = 0 #start counting ocurrence of each sighting at 0
            for j in all_sightings: 
                if i.species.name == j.species.name: #when the same species name is found
                    occurrence += 1 #add 1 to the occurrence 
                        
            dict = {'species_name': i.species.name, 'frequency': occurrence}  #create a dict with all species names and frequency of their occurrence       
            name_exists = False # set the name existing in the dictionary to false
            for name in list_dict: # loop over the names in the dictionary
                if len(list_dict)!=0: # if the length of the dictionary is not 0
                    if name["species_name"] == i.species.name: #if the name of the species is equal to the one currently being looked at 
                        name_exists = True #set name_exists to true (name exists in the dictionary)
            if name_exists == False: #if name does not exist in the dictionary 
                list_dict.append(dict) #append the name as a key to the dict


        # print(list_dict)
    print("line graph data:")

    all_birds_sighted_json = json.dumps(list_dict) 
    # print(all_birds_sighted_json)    
    
    return JsonResponse((list_dict), safe=False)

@csrf_exempt
def create_linegraph(request):

    selected_species = request.POST.getlist('species[]')
    print("REQUEST POST")
    print(request.POST.getlist('species[]'))
    print("AAAAAAAA selected species ")
    print(selected_species)

    from_date_selected = request.POST['from_date']
    to_date_selected = request.POST['to_date']
    
    from_month_start = int(str.split(from_date_selected, '-')[1])
    from_month_end = int(str.split(to_date_selected, '-')[1])

    month_diff = from_month_end-from_month_start + 1

    month_list = []

    for month in range(month_diff):
        month_list.append(from_month_start + month)
    
    # print(month_list)
    # month = request.POST['from_date']
    # print("AAAAAAAAAAAAAAAA")
    # print(from_month_start)
    # print(from_month_end)
    # print("request.POST here:")
    # print(request.POST)
    # print(selected_species)
    # print(from_date_selected)
    # print(to_date_selected)

    list_for_line_graph = [
    ]

    for each_species in selected_species:  
        # list for each selected species
        result = Species.objects.get(id=each_species) # match the id with each of the species id
        print(result)       
    
        all_sightings = Sighting.objects.filter(species = result) \
            .filter(in_country__in = request.POST.getlist('country[]')) \
            .filter(in_county__in = request.POST.getlist('county[]')) \
            .filter(date_seen__range = [from_date_selected, to_date_selected])

        single_species_list = [] # make a list for each species in the all_sighting list
        for i in all_sightings: 
            sightings_per_month = 0
            for j in all_sightings:  
                if i.date_seen.month == j.date_seen.month: 
                    sightings_per_month +=1 # increment the number of sightings by one
                
            dict = {'species_name': i.species.name, 'frequency': sightings_per_month, 'month': i.date_seen.month}
            # print('dict')
            # print(dict)
            name_exists = False 
            for elements in single_species_list: 
                print(single_species_list)
                print('elements')
                print(elements)
                # for name in elements:
                #     print('name')
                #     print(name)
                    
                if len(elements)!=0:
                    print(elements["species_name"], elements["month"])
                    print(i.species.name, i.date_seen.month)
                    if elements["species_name"] == i.species.name and elements["month"] == i.date_seen.month:
                        print("fount it!!! ")
                        name_exists = True
                        # single_species_list = [] 

            if name_exists == False:
                single_species_list.append(dict)
                # print("single_species_list")
                # print(single_species_list) 
        if single_species_list not in list_for_line_graph:
            if len(single_species_list) !=0:
                list_for_line_graph.append(single_species_list)
                single_species_list = [] 
                
        print(list_for_line_graph)
        print(month_list)       

        species_name = result.name
        for month in month_list:
            # print(month)
            month_exists = False
            
            for species_element in list_for_line_graph: 
                # print('species_element')
                # print(species_element)

                for species_sighted_per_month in species_element:
                    species_name_inside_element = species_sighted_per_month['species_name']
                    # print('species_sighted_per_month')  
                    # print(species_sighted_per_month)
                    # print(species_sighted_per_month['month'])
                    # print(month)                      
                    if month == species_sighted_per_month['month'] and species_name == species_sighted_per_month['species_name']:
                        # print("FOUND ITTTTT")
                        month_exists = True
                if month_exists == False and species_name == species_name_inside_element:        
                    dict = {'species_name': species_name, 'frequency': 0, 'month': month}
                    species_element.append(dict)
                    # print(species_element)

    # print(list_for_line_graph)

    data = {
        'line_graph_list': list_for_line_graph,
        'months': month_list
    }

    return JsonResponse((data), safe=False)


#to export data from Sightings table: 
def export(request):

    response = HttpResponse(content_type = 'text/csv')
    writer = csv.writer(response)
    writer.writerow(['Species name', 'Country', 'County', 'Date seen', 'user ID'])

    for sighting in Sighting.objects.all().values_list('species__name', 'in_country__name', 'in_county', 'date_seen', 'user'):
        writer.writerow(sighting)
    
    #to tell the browser what to do with the response: 
    response['Content-Disposition'] = 'attachment; filename="sightings.csv"'

    return response