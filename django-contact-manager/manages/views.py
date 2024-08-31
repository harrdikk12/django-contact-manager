
import logging
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from .models import Contact 
from .forms import ContactForm 
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import models

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def contact_list(request):
    try:
        contacts = Contact.objects.all()
        logger.info(f"Contacts: {contacts}")  # Log contacts
        return render(request, 'manages/contact_list.html', {'contacts': contacts})
    except Exception as e:
        logger.error(f"An error occurred: {e}")  # Log error
        return HttpResponse(f"An error occurred: {e}")

def contact_detail(request, pk):
    try:
        contact = get_object_or_404(Contact, pk=pk)
        logger.info(f"Contact: {contact}")  # Log contact
        return render(request, 'manages/contact_detail.html', {'contact': contact})
    except Exception as e:
        logger.error(f"An error occurred: {e}")  # Log error
        return HttpResponse(f"An error occurred: {e}")

def contact_create(request):
    try:
        if request.method == "POST":
            form = ContactForm(request.POST)
            if form.is_valid():
                contact = form.save()
                logger.info(f"New contact created: {contact}")  # Log new contact
                return redirect('contact_detail', pk=contact.pk)
        else:
            form = ContactForm()
        return render(request, 'manages/contact_form.html', {'form': form})
    except Exception as e:
        logger.error(f"An error occurred: {e}")  # Log error
        return HttpResponse(f"An error occurred: {e}")

def contact_edit(request, pk):
    try:
        contact = get_object_or_404(Contact, pk=pk)
        if request.method == "POST":
            form = ContactForm(request.POST, instance=contact)
            if form.is_valid():
                contact = form.save()
                logger.info(f"Contact updated: {contact}")  # Log updated contact
                return redirect('contact_detail', pk=contact.pk)
        else:
            form = ContactForm(instance=contact)
        return render(request, 'manages/contact_form.html', {'form': form})
    except Exception as e:
        logger.error(f"An error occurred: {e}")  # Log error
        return HttpResponse(f"An error occurred: {e}")
    

    
def contact_delete(request, pk):
    try:
        contact = get_object_or_404(Contact, pk=pk)
        if request.method == "POST":
            logger.info(f"Contact to be deleted: {contact}")  # Log contact to be deleted
            contact.delete()
            return redirect('contact_list')
        return render(request, 'manages/contact_confirm_delete.html', {'contact': contact})
    except Exception as e:
        logger.error(f"An error occurred: {e}")  # Log error
        return HttpResponse(f"An error occurred: {e}")
    


def validate_email(value):
    try:
        if not value.endswith('@gmail.com'):
            raise ValidationError(
                _('%(value)s is not a valid Gmail address'),
                params={'value': value},
            )
    except ValidationError as e:
        print(f"Validation error: {e}")
        raise

def validate_phone(value):
    try:
        if not value.isdigit():
            raise ValidationError(
                _('%(value)s is not a valid phone number.'),
                params={'value': value},
            )
    except ValidationError as e:
        print(f"Validation error: {e}")
        raise