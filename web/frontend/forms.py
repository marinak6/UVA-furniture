from django import forms


class CreateListingForm(forms.Form):
    name = forms.CharField(label='Name', widget=forms.TextInput)
    price = forms.DecimalField(max_digits=10, decimal_places=2)
    # Delimitted by commas
    categories = forms.CharField(
        label='Categories(Comma delimited)', widget=forms.Textarea, required=False)
    description = forms.CharField(
        label='Description', widget=forms.Textarea, required=False)


class CreateRegisterForm(forms.Form):
    first_name = forms.CharField(
        max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(
        max_length=30, required=False, help_text='Optional.')
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(label='Email', max_length=100)
