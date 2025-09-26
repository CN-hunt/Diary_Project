from django import forms
from Web import models
from Web.models import NoteBook


class DiaryForm(forms.ModelForm):
    class Meta:
        model = models.NoteBook
        fields = ('Book_Name',"description")

        widgets = {
            'Book_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
