from django.shortcuts import render
from django.http import HttpResponse
from lists.models import Item

# Create your views here.
def home_page(request):
	#if the request method is a post, crreate an item with the posted text
	if request.method == 'POST':
		new_item_text = request.POST['item_text']
		Item.objects.create(text=new_item_text)
	else:
		new_item_text = ''

	return render(request, 'home.html',{
		'new_item_text': request.POST.get('item_text', ''),
		})
