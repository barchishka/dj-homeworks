from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
import csv


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    with open('data-398-2018-08-30.csv', encoding='utf-8', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        baza = []
        for bz in reader:
            baza.append({'Name': bz['Name'],
                         'Street': bz['Street'],
                         'District': bz['District']})
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице
    paginator = Paginator(baza, 15)
    page_num = request.GET.get("page", 1)
    page = paginator.get_page(page_num)
    data = page.object_list
    context = {
        'bus_stations': data,
        'page': page
    }

    return render(request, 'stations/index.html', context)
