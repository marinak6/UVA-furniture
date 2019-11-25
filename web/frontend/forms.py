from django import forms


class CreateListingForm(forms.Form):
    name = forms.CharField(label='Name',
                           widget=forms.TextInput(attrs={'id': 'create_name', 'class': 'form-control'}))

    price = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.TextInput(
        attrs={'id': 'create_price', 'class': 'form-control'}))
    # Delimitted by commas
    category = forms.CharField(
        label='Category(Comma delimited for multiple)', required=False, widget=forms.TextInput(attrs={'id': 'create_category', 'class': 'form-control'}))
    description = forms.CharField(
        label='Description', required=False, widget=forms.TextInput(attrs={'id': 'create_description', 'class': 'form-control'}))


class CreateRegisterForm(forms.Form):
    first_name = forms.CharField(label='First Name',
                                 max_length=30, required=False, widget=forms.TextInput(attrs={'id': 'id_first_name', 'class': 'form-control'}))
    last_name = forms.CharField(label='Last Name',
                                max_length=30, required=False, widget=forms.TextInput(attrs={'id': 'id_last_name', 'class': 'form-control'}))
    password = forms.CharField(
        label='Password', widget=forms.PasswordInput(attrs={'id': 'id_password', 'class': 'form-control'}))
    email = forms.EmailField(label='Email', max_length=100, widget=forms.TextInput(
        attrs={'id': 'id_email', 'class': 'form-control'}))
