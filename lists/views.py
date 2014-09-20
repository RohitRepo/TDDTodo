from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Item, List

def home_page(request):

    return render(request, 'home.html')

def view_list(request, list_id):
    items = Item.objects.filter(list=list_id)
    item_list = List.objects.get(id=list_id) 
    return render(request, 'list.html', {'items': items, 'list': item_list})

def new_list(request):
    new_item_text = request.POST['item_text']
    new_list = List.objects.create()
    new_item = Item.objects.create(text=new_item_text, list=new_list)
    return redirect('/lists/%d/' %(new_list.id,))

def add_item(request, list_id):
    item_list = List.objects.get(id=list_id)
    new_item = Item.objects.create(text = request.POST['item_text'], list=item_list)
    return redirect('/lists/%d/' %(item_list.id,))

