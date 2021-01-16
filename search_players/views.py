from django.shortcuts import render, redirect
from django.http import HttpResponse
from search_players.forms import SearchPlayersForm
from urllib.parse import urlencode
from utils.utils import Player, TeammateService



def home(request):
    if request.method == 'POST':
        returned_form = SearchPlayersForm(request.POST)
        if returned_form.is_valid():
            players = {
                'p_one': request.POST['p_one'],
                'p_two': request.POST['p_two']
            }
            query_string =  urlencode(players)
            base_url = 'results/'
            url = '{}?{}'.format(base_url, query_string)
        return redirect(url)
    form = SearchPlayersForm()
    ctx = {
        'header': 'Search Players',
        'form': form
    }
    return render(request, 'search_players/home.html', ctx)

def return_search_results(request):
    teammate_service = TeammateService([
        request.GET.get('p_one'),
        request.GET.get('p_two')
    ])
    players = teammate_service.generate_players()
    # teammates = teammate_service.calculate_mutual_teammates()
    if not players:
        ctx = {
            'header': 'Error In Player Search'
        }
        return render(request, 'search_players/results.html', ctx)

    # generalise logic such that we can find the mutual teammates of
    # multiple players
    p_one = players[0]
    p_two = players[1]
    teammates = p_one.generate_mutual_teammates(p_two)
    ctx = {
        'teammates': teammates,
        'header': 'Search Players Results'
    }
    return render(request, 'search_players/results.html', ctx)

