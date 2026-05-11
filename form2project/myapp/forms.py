from django import forms
class StudentForm(forms.Form):
    name=forms.CharField()
    age=forms.IntegerField()
    place=forms.CharField()
    email=forms.EmailField()

def clean_name(self):
        name=self.cleaned_data['name']
        if len(name)<5:
            raise forms.ValidationError('Name should have atleast 5 characters')
        return name