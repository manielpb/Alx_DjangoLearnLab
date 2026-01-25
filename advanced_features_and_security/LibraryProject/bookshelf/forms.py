from django import forms

class BookSearchForm(forms.Form):
    q = forms.CharField(required=False, max_length=100)

    def clean_q(self):
        q = self.cleaned_data["q"].strip()
        return q