from django import forms
from .models import Genre, Movie, People, Comment, Score

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'

class PeopleForm(forms.ModelForm):
    class Meta:
        model = People
        fields = '__all__'
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content',]
        
class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['value',]