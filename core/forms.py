from django import forms

class ParagraphForm(forms.Form):
    text = forms.CharField(label='text', required=True)