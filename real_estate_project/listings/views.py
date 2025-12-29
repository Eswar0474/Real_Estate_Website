from itertools import chain
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Max, Subquery, When, Case, OuterRef, F
from django.db.models.functions import Coalesce
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .forms import PropertyForm
from .models import Property, PropertyImage
import random
from .models import MessageModel
from django.contrib import messages
from decimal import Decimal
def home(request):
    # --- Existing Logic ---
    showcase_property = Property.objects.filter(is_published=True, property_type='House').order_by('-price').first()
    featured_houses = Property.objects.filter(is_published=True, property_type='House').order_by('-list_date')[:4]
    featured_land = Property.objects.filter(is_published=True, property_type='Land').order_by('-list_date')[:4]

    # --- Recommendation Logic with Django Messages ---
    recommended_properties = []
    if request.user.is_authenticated:
        profile = getattr(request.user, 'profile', None)

        has_recommendation_criteria = False
        query = Q(is_published=True)

        if profile:
            if profile.budget and profile.budget > 0:
                min_price = profile.budget * Decimal('0.80')
                max_price = profile.budget * Decimal('1.20')
                query &= Q(price__gte=min_price, price__lte=max_price)
                has_recommendation_criteria = True

            if profile.preferred_location:
                query &= Q(location__icontains=profile.preferred_location)
                has_recommendation_criteria = True


            if has_recommendation_criteria:
                recommended_properties = Property.objects.filter(query).exclude(
                    pk=showcase_property.pk if showcase_property else None
                ).order_by('?')[:4]

                # If the final list is empty, add a warning message
                if not recommended_properties:
                    messages.warning(request, "We couldn't find any properties that match your budget or location preferences. Try updating your profile!")

    context = {
        'showcase_property': showcase_property,
        'featured_houses': featured_houses,
        'featured_land': featured_land,
        'recommended_properties': recommended_properties,
    }
    return render(request, 'listings/home.html', context)


@login_required
def seller_dashboard(request):
    """
    View for the seller's dashboard.
    Displays properties listed by the currently logged-in user.
    """
    # Initialize the queryset for properties
    listed_properties = Property.objects.none()

    try:
        # Filter properties to get only those created by the current user
        # We need to add a 'seller' field to the Property model first.
        # For now, let's assume it exists.
        listed_properties = Property.objects.filter(seller=request.user).order_by('-list_date')
    except Exception as e:
        messages.error(request, "An error occurred while fetching your properties.")
        # Log the error for debugging
        # import logging
        # logging.error(f"Error in seller_dashboard: {e}")

    context = {
        'listed_properties': listed_properties,
    }
    return render(request, 'listings/seller_dashboard.html', context)

# (Your other views like property_detail, property_search remain here...)
def property_detail(request, pk):
    """
    View to display the details of a single property and handle message sending.
    """
    property_obj = get_object_or_404(Property, pk=pk, is_published=True)
    additional_images = property_obj.images.all()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to send a message.')
            return redirect('users:login')

        message_body = request.POST.get('message_body', '').strip()

        if property_obj.seller == request.user:
            messages.error(request, "You cannot send a message to yourself.")
            return redirect('listings:property-detail', pk=pk)

        if message_body:
            # Use the aliased model name 'MessageModel'
            MessageModel.objects.create(
                sender=request.user,
                recipient=property_obj.seller,
                property=property_obj,
                body=message_body
            )
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('listings:property-detail', pk=pk)
        else:
            messages.error(request, 'You cannot send an empty message.')

    context = {
        'property': property_obj,
        'additional_images': additional_images,
    }
    return render(request, 'listings/property_detail.html', context)


@login_required
def add_property_view(request):
    """
    View for sellers to add a new property.
    """
    if request.method == 'POST':
        # If the form is submitted, process the data
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            # Don't save to the database just yet
            property_instance = form.save(commit=False)
            # Assign the currently logged-in user as the seller
            property_instance.seller = request.user
            # Now, save the complete instance to the database
            property_instance.save()
            messages.success(request, 'Your property has been listed successfully!')
            return redirect('listings:seller-dashboard')
        else:
            # If the form is not valid, show an error message
            messages.error(request, 'Please correct the errors below.')
    else:
        # If it's a GET request, just display a blank form
        form = PropertyForm()

    context = {
        'form': form
    }
    return render(request, 'listings/add_property.html', context)

@login_required
def edit_property_view(request, pk):
    """
    View for a seller to edit one of their existing properties.
    """
    # Fetch the property instance, ensuring it belongs to the current user
    property_instance = get_object_or_404(Property, pk=pk, seller=request.user)

    if request.method == 'POST':
        # Pass the instance to the form to pre-populate it and update it
        form = PropertyForm(request.POST, request.FILES, instance=property_instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your property has been updated successfully!')
            return redirect('listings:seller-dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # If it's a GET request, create the form pre-filled with the property's data
        form = PropertyForm(instance=property_instance)

    context = {
        'form': form,
        'property': property_instance  # Pass property to the template for context
    }
    return render(request, 'listings/edit_property.html', context)

@login_required
def confirm_delete_property_view(request, pk):
    """
    Displays a confirmation page before deleting a property.
    This view only handles GET requests.
    """
    # Fetch the property to make sure it exists and belongs to the user
    property_instance = get_object_or_404(Property, pk=pk, seller=request.user)
    context = {
        'property': property_instance
    }
    return render(request, 'listings/confirm_delete.html', context)

# --- UPDATED: The actual delete logic, now simplified and more secure ---
@login_required
@require_POST  # This decorator is crucial for security
def delete_property_view(request, pk):
    """
    Handles the actual deletion of a property after confirmation.
    This view only accepts POST requests.
    """
    property_instance = get_object_or_404(Property, pk=pk, seller=request.user)
    try:
        title = property_instance.title
        property_instance.delete()
        messages.success(request, f'The property "{title}" was deleted successfully.')
    except Exception as e:
        messages.error(request, f'An error occurred while trying to delete the property: {e}')

    return redirect('listings:seller-dashboard')

@login_required
def inbox_view(request):
    """
    Displays a list of unique conversations, each represented by its
    single latest message.
    """
    user = request.user

    # This subquery finds the ID of the latest message for each conversation partner.
    latest_message_subquery = MessageModel.objects.filter(
        Q(sender=OuterRef('other_user'), recipient=user) |
        Q(sender=user, recipient=OuterRef('other_user'))
    ).order_by('-timestamp').values('pk')[:1] # Get the PK of the latest one

    # Get all unique conversation partners and annotate with the latest message ID
    conversations = MessageModel.objects.filter(
        Q(sender=user) | Q(recipient=user)
    ).annotate(
        # First, identify the 'other user' in the conversation
        other_user=Case(
            When(sender=user, then=F('recipient')),
            default=F('sender')
        )
    ).values('other_user').distinct().annotate(
        # Annotate each unique partner with the ID of our latest message
        latest_message_pk=Subquery(latest_message_subquery)
    )

    # Finally, get the actual message objects for the latest messages
    latest_messages = MessageModel.objects.filter(
        pk__in=[c['latest_message_pk'] for c in conversations]
    ).order_by('-timestamp')

    context = {
        'conversations': latest_messages
    }
    return render(request, 'listings/inbox.html', context)


@login_required
def conversation_view(request, user_id):
    """
    Displays the full message thread between the current user and another user.
    """
    other_user = get_object_or_404(User, id=user_id)

    messages_thread = MessageModel.objects.filter(
        (Q(sender=request.user) & Q(recipient=other_user)) |
        (Q(sender=other_user) & Q(recipient=request.user))
    ).order_by('timestamp')

    messages_thread.filter(recipient=request.user).update(is_read=True)

    if request.method == 'POST':
        body = request.POST.get('body', '').strip()
        if body:
            MessageModel.objects.create(
                sender=request.user,
                recipient=other_user,
                body=body,
            )
            return redirect('listings:conversation-detail', user_id=user_id)

    context = {
        'messages_thread': messages_thread,
        'other_user': other_user
    }
    return render(request, 'listings/conversation_detail.html', context)

@login_required
def property_list(request):
    """
    This view handles the main buyer page, including the featured
    slideshow and filtering for the property grid.
    """
    # Get the filter type from the URL (e.g., ?type=House)
    property_type_filter = request.GET.get('type')

    # --- Prepare data for the main property grid ---
    properties_list = Property.objects.filter(is_published=True).order_by('-list_date')
    if property_type_filter in ['House', 'Land']:
        properties_list = properties_list.filter(property_type=property_type_filter)

    # --- Prepare data for the "Best Properties" slideshow ---
    # To give equal priority, we get the top 2 of each type
    top_houses = Property.objects.filter(property_type='House', is_published=True).order_by('-price')[:2]
    top_lands = Property.objects.filter(property_type='Land', is_published=True).order_by('-price')[:2]

    # Combine the querysets and sort by price to get the final featured list
    featured_properties = sorted(
        list(chain(top_houses, top_lands)),
        key=lambda instance: instance.price,
        reverse=True
    )

    context = {
        'properties': properties_list,
        'featured_properties': featured_properties,
        'active_filter': property_type_filter,  # To highlight the active button
    }
    return render(request, 'listings/property_list.html', context)

@login_required
def toggle_favorite(request, pk):
    property = get_object_or_404(Property, pk=pk)
    profile = request.user.profile

    if property in profile.wishlist.all():
        # Remove from favorites
        profile.wishlist.remove(property)
    else:
        # Add to favorites
        profile.wishlist.add(property)

    # Redirect back to the previous page or a default
    return redirect(request.META.get('HTTP_REFERER', 'property-list'))


def help_center_view(request):
    return render(request, 'listings/help_center.html')