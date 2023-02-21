from django import forms
from django.contrib.admin import widgets
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


from .models import Post, Author, Venue, Category, Conference


class PostForm(forms.ModelForm):

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'}))
    overview = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control'}))
    authors = forms.ModelMultipleChoiceField(
        queryset=Author.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    venue = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Venue.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    citation = forms.URLField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'}))
    pdf = forms.URLField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'}))
    supplement = forms.URLField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'}))
    slides = forms.URLField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'}))
    poster = forms.URLField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'}))
    code = forms.URLField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'}))
    video = forms.URLField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'}))

    class Meta:
        model = Post
        fields = ['title',
                  'overview',
                  'authors',
                  'thumbnail',
                  'categories',
                  'venue',
                  'citation',
                  'pdf',
                  'supplement',
                  'slides',
                  'poster',
                  'code',
                  'video']

        labels = {'title': 'Title',
                  'overview': 'TLDR',
                  'authors': 'Authors',
                  'thumbnail': 'Image',
                  'categories': 'Categories',
                  'venue': 'Venue',
                  'citation': 'Citation',
                  'pdf': 'Pdf Link',
                  'supplement': 'Supplement',
                  'slides': 'Slides',
                  'poster': 'Poster',
                  'code': 'Code',
                  'video': 'Video'}


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['user', 'user_url']
        labels = ['name', 'url']


class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['venue_name', 'year', 'venue_url']
        labels = ['Name', 'Year', 'URL']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["title"]
        labels = ['Title']


class ArxivForm(forms.Form):
    link = forms.CharField(max_length=200)


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class ConferenceForm(forms.ModelForm):

    date_formats = [
        '%Y-%m-%d',  # '2006-10-25'
        '%m/%d/%Y',  # '10/25/2006'
        '%m/%d/%y',  # '10/25/06'
        '%b %d %Y',  # 'Oct 25 2006'
        '%b %d, %Y',  # 'Oct 25, 2006'
        '%d %b %Y',  # '25 Oct 2006'
        '%d %b, %Y',  # '25 Oct, 2006'
        '%B %d %Y',  # 'October 25 2006'
        '%B %d, %Y',  # 'October 25, 2006'
        '%d %B %Y',  # '25 October 2006'
        '%d %B, %Y',  # '25 October, 2006'
        '%d %b',
        '%d %B'
    ]

    link = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'conference_link form-control'})
    )

    name = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    start_date = forms.DateField(
        required=False,
        input_formats=date_formats,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    end_date = forms.DateField(
        required=False,
        input_formats=date_formats,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    location = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Conference
        fields = ['link', 'name', 'start_date', 'end_date', 'location']
        labels = {
            'name': 'Name',
            'link': 'Conference Link',
            'location': 'Location',
            'start_date': 'Starting on',
            'end_date': 'To'
        }