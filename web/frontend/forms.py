from django import forms


class CreateListingForm(forms.Form):
    name = forms.CharField(label='Name',
                           widget=forms.TextInput(attrs={'class': 'form-control'}))

    price = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    # Delimitted by commas
    category = forms.CharField(
        label='Category(Comma delimited for multiple)', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(
        label='Description', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))


class CreateRegisterForm(forms.Form):
    first_name = forms.CharField(
        max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(
        max_length=30, required=False, help_text='Optional.')
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(label='Email', max_length=100)
