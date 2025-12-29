from django import forms
from .models import Property

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        # List all fields from the model that the user should fill out.
        # 'seller' is excluded because we will set it automatically in the view.
        # 'is_published' is also excluded as we might want to control that differently.
        fields = [
            'title', 'description', 'price', 'property_type', 'status',
            'bedrooms', 'bathrooms', 'area_sqft', 'location', 'facing',
            'main_image'
        ]

        # You can add widgets to customize the form fields' appearance
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'description': forms.Textarea(attrs={'class': 'w-full p-2 border rounded', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded'}),
            'property_type': forms.Select(attrs={'class': 'w-full p-2 border rounded', 'id': 'id_property_type'}),
            'status': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
            'bedrooms': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded'}),
            'bathrooms': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded'}),
            'area_sqft': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded'}),
            'location': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'facing': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'e.g., South, East'}),
            'main_image': forms.FileInput(attrs={'class': 'w-full p-2 border rounded'}),
        }