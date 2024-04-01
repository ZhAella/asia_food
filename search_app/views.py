from django.shortcuts import render
from django.views import View
from delivery.models import Food, Drink
from django.contrib.postgres.search import (SearchQuery,
                                            SearchVector,
                                            SearchRank)
from . import models, forms, search


class SearchView(View):
    @staticmethod
    def get(request):
        query = SearchQuery(request.GET['query'])
        vector = SearchVector('name')
        rank = SearchRank(vector=vector, query=query)
        food_results = (Food.objects.annotate(rank=rank).
                        filter(rank__gt=0).
                        order_by('-rank').
                        values_list('id', 'name', 'rank'))
        drink_results = (Drink.objects.annotate(rank=rank).
                         filter(rank__gt=0).
                         order_by('-rank').
                         values_list('id', 'name', 'rank'))

        return render(request,
                      'search_app/search_results.html',
                      {'food_results': food_results,
                       'drink_results': drink_results}
                      )
