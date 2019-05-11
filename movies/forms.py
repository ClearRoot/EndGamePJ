from django import forms
from .models import Genre, Movie, MovieRank, People, Comment, Score, MovieDip

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'

class PeopleForm(forms.ModelForm):
    class Meta:
        model = People
        fields = '__all__'
        
class MovieRankForm(forms.ModelForm):
    class Meta:
        model = MovieRank
        fields = '__all__'
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content',]
        
class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['value',]
        
class MovieDipForm(forms.ModelForm):
    class Meta:
        model = MovieDip
        fields = ['movie',]