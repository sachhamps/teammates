from django import forms

class SearchPlayersForm(forms.Form):
    p_one = forms.CharField(widget=forms.TextInput(
        attrs={
            'input id': 'inputPlayer1',
            'class': 'form-control',
            'placeholder': 'Player 1',
        }
    ))
    p_two = forms.CharField(widget=forms.TextInput(
        attrs={
            'input id': 'inputPlayer2',
            'class': 'form-control',
            'placeholder': 'Player 2',
        }
    ))