from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Crop, UserPrediction

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class CropForm(forms.ModelForm):
    # Add validators to fields
    name = forms.CharField(max_length=100, required=True)
    nitrogen = forms.FloatField(
        validators=[MinValueValidator(0.0, "Nitrogen value must be positive")],
        widget=forms.NumberInput(attrs={'step': '0.01'})
    )
    phosphorous = forms.FloatField(
        validators=[MinValueValidator(0.0, "Phosphorous value must be positive")],
        widget=forms.NumberInput(attrs={'step': '0.01'})
    )
    potash = forms.FloatField(
        validators=[MinValueValidator(0.0, "Potash value must be positive")],
        widget=forms.NumberInput(attrs={'step': '0.01'})
    )
    rainfall = forms.FloatField(
        validators=[MinValueValidator(0.0, "Rainfall must be positive")],
        widget=forms.NumberInput(attrs={'step': '0.1'})
    )
    temperature = forms.FloatField(
        validators=[
            MinValueValidator(-50.0, "Temperature must be above -50°C"),
            MaxValueValidator(60.0, "Temperature must be below 60°C")
        ],
        widget=forms.NumberInput(attrs={'step': '0.1'})
    )
    soil_ph = forms.FloatField(
        validators=[
            MinValueValidator(0.0, "pH must be between 0 and 14"),
            MaxValueValidator(14.0, "pH must be between 0 and 14")
        ],
        widget=forms.NumberInput(attrs={'step': '0.1'})
    )
    
    class Meta:
        model = Crop
        fields = ['name', 'nitrogen', 'phosphorous', 'potash', 'rainfall', 'temperature', 'soil_ph', 'image', 'description']
        
    def __init__(self, *args, **kwargs):
        super(CropForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            
    def clean_name(self):
        name = self.cleaned_data.get('name')
        # Check if name exists (when creating a new crop)
        if not self.instance.pk:
            if Crop.objects.filter(name=name).exists():
                raise forms.ValidationError(f"A crop with the name '{name}' already exists.")
        return name

class PredictionForm(forms.ModelForm):
    # Add validators to fields
    nitrogen = forms.FloatField(
        validators=[MinValueValidator(0.0, "Nitrogen value must be positive")],
        widget=forms.NumberInput(attrs={'step': '0.01'})
    )
    phosphorous = forms.FloatField(
        validators=[MinValueValidator(0.0, "Phosphorous value must be positive")],
        widget=forms.NumberInput(attrs={'step': '0.01'})
    )
    potash = forms.FloatField(
        validators=[MinValueValidator(0.0, "Potash value must be positive")],
        widget=forms.NumberInput(attrs={'step': '0.01'})
    )
    rainfall = forms.FloatField(
        validators=[MinValueValidator(0.0, "Rainfall must be positive")],
        widget=forms.NumberInput(attrs={'step': '0.1'})
    )
    temperature = forms.FloatField(
        validators=[
            MinValueValidator(-50.0, "Temperature must be above -50°C"),
            MaxValueValidator(60.0, "Temperature must be below 60°C")
        ],
        widget=forms.NumberInput(attrs={'step': '0.1'})
    )
    soil_ph = forms.FloatField(
        validators=[
            MinValueValidator(0.0, "pH must be between 0 and 14"),
            MaxValueValidator(14.0, "pH must be between 0 and 14")
        ],
        widget=forms.NumberInput(attrs={'step': '0.1'})
    )
    
    class Meta:
        model = UserPrediction
        fields = ['nitrogen', 'phosphorous', 'potash', 'rainfall', 'temperature', 'soil_ph']
        
    def __init__(self, *args, **kwargs):
        super(PredictionForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})