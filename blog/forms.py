from django import forms

class SearchForm(forms.Form):
    title=forms.CharField(max_length=100,label="Search")
    #,placeholder="Search by tags/title"