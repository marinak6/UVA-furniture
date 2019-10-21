from django import forms


class CreateListingForm(forms.Form):
    name = forms.CharField(label='Name', widget=forms.TextInput)
    price = forms.DecimalField(max_digits=10, decimal_places=2)
    # Delimitted by commas
    category = forms.CharField(
        label='Category(Comma delimited for multiple)', widget=forms.Textarea, required=False)
    description = forms.CharField(
        label='Description', widget=forms.Textarea, required=False)
