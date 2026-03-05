from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignUpForm, CropForm, PredictionForm
from .models import Crop, UserPrediction
from .ml_model import predict_crop

def is_admin(user):
    return user.is_staff or user.is_superuser

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('user_dashboard')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def user_dashboard(request):
    return render(request, 'user/dashboard.html')

@login_required
def crop_review(request):
    crops = Crop.objects.all()
    return render(request, 'user/crop_review.html', {'crops': crops})

@login_required
def crop_details(request, crop_id):
    crop = get_object_or_404(Crop, pk=crop_id)
    return render(request, 'user/crop_details.html', {'crop': crop})

@login_required
def crop_prediction(request):
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            prediction = form.save(commit=False)
            prediction.user = request.user
            
            # Make prediction
            predicted_crop = predict_crop(
                prediction.nitrogen,
                prediction.phosphorous,
                prediction.potash,
                prediction.rainfall,
                prediction.temperature,
                prediction.soil_ph
            )
            
            prediction.predicted_crop = predicted_crop
            prediction.save()
            
            # Get the crop object for display
            try:
                crop = Crop.objects.get(name=predicted_crop)
                return render(request, 'user/prediction_result.html', {'prediction': prediction, 'crop': crop})
            except Crop.DoesNotExist:
                return render(request, 'user/prediction_result.html', {'prediction': prediction, 'crop': None})
    else:
        form = PredictionForm()
    
    return render(request, 'user/crop_prediction.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    crops = Crop.objects.all()
    return render(request, 'admin/dashboard.html', {'crops': crops})

@login_required
@user_passes_test(is_admin)
def add_crop(request):
    if request.method == 'POST':
        form = CropForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Crop added successfully!')
            return redirect('admin_dashboard')
    else:
        form = CropForm()
    
    return render(request, 'admin/add_crop.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def update_crop(request, crop_id):
    crop = get_object_or_404(Crop, pk=crop_id)
    
    if request.method == 'POST':
        form = CropForm(request.POST, request.FILES, instance=crop)
        if form.is_valid():
            form.save()
            messages.success(request, 'Crop updated successfully!')
            return redirect('admin_dashboard')
    else:
        form = CropForm(instance=crop)
    
    return render(request, 'admin/update_crop.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def delete_crop(request, crop_id):
    crop = get_object_or_404(Crop, pk=crop_id)
    
    if request.method == 'POST':
        crop.delete()
        messages.success(request, 'Crop deleted successfully!')
        return redirect('admin_dashboard')
    
    return render(request, 'admin/delete_crop.html', {'crop': crop})