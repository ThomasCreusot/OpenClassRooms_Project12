from django.shortcuts import render

from customerRelationshipManagement_app.models import Client

# Create your views here.
def index(request):
    obj = Client.objects.all()
    context={
        "obj": obj,
    }
    return render(request, 'index.html', context=context)