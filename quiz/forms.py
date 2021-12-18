from django import forms


class UserAnswer(forms.Form):
    answer = forms.CharField(
        label="Your Answer Here", required=True)
