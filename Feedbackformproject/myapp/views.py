from django.shortcuts import render, redirect
from django.contrib import messages
from myapp.forms import Feedbackform


def formview(request):
    """Handle feedback form display and submission"""
    if request.method == "POST":
        form =Feedbackform(request.POST)
        if form.is_valid():
            # Save form data to database
            form.save()
            messages.success(request, "Feedback submitted successfully!")
            return redirect('form')  # Redirect to clear form
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = Feedbackform()
    
    return render(request, 'form.html', {'form': form})
