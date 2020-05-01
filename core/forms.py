from django import forms

class ParagraphForm(forms.Form):
    text = forms.CharField(label='text', required=True)
class SliceForm(forms.Form):
    text = forms.CharField(label='text', required=True)
    number = forms.IntegerField(label='number',required=True,max_value=5,min_value=1) 