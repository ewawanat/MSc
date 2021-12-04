from django.shortcuts import render


def homePage(request):
#    return HttpResponse('Hi there birder!')
    return render(request, 'homepage.html')
