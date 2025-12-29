from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib import messages

from .forms import UserSettingsForm, ProfileSettingsForm, CustomSetPasswordForm, PasswordResetVerificationForm
from .models import Profile  # Make sure you have the Profile model from your description


def register_view(request):
    """
    Handles user registration. On POST, it creates a new User, a Profile,
    and assigns them to either a 'Sellers' or 'Buyers' group.
    """
    # Ensure 'Sellers' and 'Buyers' groups exist. Create them if they don't.
    # This is often done in a post-migration signal, but is here for simplicity.
    seller_group, _ = Group.objects.get_or_create(name='Sellers')
    buyer_group, _ = Group.objects.get_or_create(name='Buyers')

    if request.method == 'POST':
        # Get form data from the request
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile_number = request.POST.get('mobile_number')
        email = request.POST.get('email')
        password = request.POST.get('password')
        location = request.POST.get('preferred_location')
        user_type = request.POST.get('user_type')  # 'seller' or 'buyer'

        # --- Validation ---
        if User.objects.filter(username=email).exists():
            messages.error(request, 'An account with this email already exists.')
            return redirect('users:register')  # Redirect back to the registration page

        # In a real app, you would add more validation here (e.g., for password strength)

        # --- User Creation ---
        # We use the email as the username for simplicity
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # --- Profile and Group Assignment ---
        # The mobile number isn't on the default User or Profile model you provided,
        # so we'll just assign the location to the profile.
        Profile.objects.create(user=user, preferred_location=location)

        if user_type == 'seller':
            user.groups.add(seller_group)
        else:
            user.groups.add(buyer_group)

        user.save()

        # After successful registration, send them to the login page with a message
        messages.success(request, 'Registration successful! Please log in.')
        return redirect('users:login')

    # For a GET request, just show the registration page (index.html)
    return render(request, 'index.html')


def login_view(request):
    """
    Handles user login. On POST, it authenticates the user and, if successful,
    redirects them to the appropriate dashboard based on their group.
    """
    if request.method == 'POST':
        # Determine if it's a seller or buyer login from the form submission
        user_role = 'buyer'  # Default
        if 'seller-login' in request.POST:  # A way to distinguish forms
            user_role = 'seller'

        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate user
        # Note: Django's authenticate uses 'username', so we pass the email for it
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            # Check user group and redirect
            if user_role == 'seller':
                return redirect('listings:seller-dashboard')
            elif user_role == 'buyer':
                return redirect('listings:property-list')
            else:
                # Fallback for users with no group (e.g., admin)
                messages.error(request, 'Your account does not have an assigned role.')
                return redirect('users:login')
        else:
            # Invalid login
            messages.error(request, 'Invalid email or password.')
            return redirect('users:login')

    # For a GET request, just show the login page
    return render(request, 'login.html')


def seller_page_view(request):
    """Renders the seller dashboard page."""
    # Add authentication check to protect this page
    if not request.user.is_authenticated or not request.user.groups.filter(name='Sellers').exists():
        return redirect('login')
    return redirect('listings:seller-dashboard')


def buyer_page_view(request):
    """Renders the buyer home page."""
    # Add authentication check to protect this page
    if not request.user.is_authenticated or not request.user.groups.filter(name='Buyers').exists():
        return redirect('login')
    return render(request, 'buyer.html')


def logout_view(request):
    """Logs the user out and redirects to the login page."""
    logout(request)
    messages.info(request, 'You have been successfully logged out.')
    return redirect('users:login')
@login_required
def settings_view(request):
    # Get or create the user's profile
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserSettingsForm(request.POST, instance=request.user)
        profile_form = ProfileSettingsForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your settings have been updated successfully!')
            return redirect('users:settings')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserSettingsForm(instance=request.user)
        profile_form = ProfileSettingsForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'settings.html', context)
def password_reset_verify_view(request):
    """
    Step 1: Handles the verification of user details.
    """
    if request.method == 'POST':
        form = PasswordResetVerificationForm(request.POST)
        if form.is_valid():
            # The user's identity is verified. Store their ID in the session
            # so we know who is resetting their password on the next page.
            user = form.user
            request.session['password_reset_user_id'] = user.id
            return redirect('users:password-reset-confirm')
    else:
        form = PasswordResetVerificationForm()

    return render(request, 'password_reset_verify.html', {'form': form})


def password_reset_confirm_view(request):
    """
    Step 2: Handles the actual password reset for the verified user.
    """
    user_id = request.session.get('password_reset_user_id')
    if not user_id:
        # If there's no user ID in the session, they haven't completed step 1.
        messages.error(request, 'Verification step was missed. Please verify your identity first.')
        return redirect('users:password-reset-verify')

    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        form = CustomSetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            # Clear the session variable after a successful reset
            del request.session['password_reset_user_id']
            messages.success(request, 'Your password has been successfully reset. You can now log in with your new password.')
            return redirect('users:login')
    else:
        form = CustomSetPasswordForm(user)

    return render(request, 'password_reset_confirm.html', {'form': form})
@login_required
def password_reset(request,id):
    """
    Step 2: Handles the actual password reset for the verified user.
    """
    user_id = id
    if not user_id:
        # If there's no user ID in the session, they haven't completed step 1.
        return redirect('listings:home')
    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        form = CustomSetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password has been successfully reset.')
            return redirect('users:login')
    else:
        form = CustomSetPasswordForm(user)

    return render(request, 'password_reset_confirm.html', {'form': form})


