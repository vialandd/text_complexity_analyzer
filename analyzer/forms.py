from django import forms
from .models import TextDocument


class TextDocumentForm(forms.ModelForm):
    class Meta:
        model = TextDocument
        fields = ["title", "category", "content", "tags"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 10}),
            "tags": forms.SelectMultiple(attrs={"class": "form-select"}),
        }
