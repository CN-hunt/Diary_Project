from django import forms
from Web import models
from Web.models import NoteBook


class DiaryForm(forms.ModelForm):
    class Meta:
        model = models.NoteBook
        fields = ('Book_Name', "description")

        widgets = {
            'Book_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }


class DiaryContentForm(forms.ModelForm):

    class Meta:
        model = models.DiaryContents
        fields = ('title', 'content', 'weather')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'weather': forms.Select(attrs={'class': 'form-control'}),
        }
