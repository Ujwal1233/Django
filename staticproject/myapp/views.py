from django.shortcuts import render

# Create your views here.
def myview(request):
    name="Rama"
    bird="Peacock"
    animal="lion"
    dish="biryani"
    ctx={"name":name,"bird":bird,"animal":animal,"dish":dish}
    return render(request,"myapp/fav.html",ctx)