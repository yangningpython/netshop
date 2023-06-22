from django.shortcuts import render

# Create your views here.
from django.views import View
class ShowloveView(View):

    def get(self,request):
        return render(request, 'showLove.html')