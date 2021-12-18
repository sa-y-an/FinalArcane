from django import forms


class UserDetails(forms.Form):
    full_name = forms.CharField(max_length=400, label="Enter Your Full Name")
    college = forms.CharField(max_length=400, label="Enter Your college name")
    year = forms.IntegerField(min_value=1, max_value=4,
                              label="Enter your studying year")
    contact = forms.CharField(
        min_length=10, max_length=10, label="Enter your Phone Number", required=False)
