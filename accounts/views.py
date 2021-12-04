from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout

def signup_view(request):
    if request.method =='POST':
        #to validate the data from the signup form:
        form = UserCreationForm(request.POST) #pass the request object with the information about the request and .POST accesses the post data, i.e. data that was supplied in the form
        #returns a valid or invalid form and if valid the user is saved to database:
        if form.is_valid():
            user = form.save() # form.save() returns the user, so is saved in user variable
            #log the user in:
            login(request, user)
            return redirect('enterdata:enterdata')
    else:
        form = UserCreationForm() #creating a new instance of the user form    
    return render(request, 'accounts/signup.html', {'form': form}) #third parameter passed is the form which is then sent to the template


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST) #validate the data, i.e. check the username and password are correct
        if form.is_valid():
            #log in the user
            user = form.get_user() #get the user name
            login(request, user)
            return redirect('enterdata:enterdata')

    else:
        #for when the user clicks on the login link (GET request)
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form':form})
    

def logout_view(request):
    #has to be a POST request 
    if request.method == 'POST':
        logout(request)
        return redirect('homepage')
