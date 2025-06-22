'''
Views for user profile management,
including viewing, editing, and updating user profiles.
from django.conf import settings
'''
from datetime import date

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.utils import timezone

from allauth.account.models import EmailAddress
from allauth.account.utils import send_email_confirmation

from userprofile.models import UserProfile

# pylint: disable=no-member

now = timezone.now()


@login_required
def profileedit(request):
    """Render the user profile page with profile information."""
    user = request.user
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)

    profile_data = {
        'profile_picture': (
            profile.profile_picture.url if profile.profile_picture else None
        ),
        'bio': profile.bio,
        'location': profile.location,
        'date_of_birth': profile.date_of_birth,
    }

    context = {
        'user': user,
        'profile': profile_data
    }
    return render(request, 'userprofile/profile.html', context=context)


@login_required
def upload_profile_picture(request):
    """Upload a profile picture for the user."""
    if request.method == 'POST':
        profile = UserProfile.objects.get(user=request.user)
        profile_picture = request.FILES.get('profile_picture')
        if profile_picture:
            if profile.profile_picture:
                profile.profile_picture.delete(save=True)
            profile.profile_picture = profile_picture
            profile.save()
            messages.success(request, "Profile picture updated successfully.")
        else:
            messages.error(request, "No profile picture provided.")
    else:
        messages.error(request, "Failed to update profile picture.")
    return redirect('profile')


@login_required
def delete_profile_picture(request):
    """Delete the user's profile picture."""
    if request.method == 'POST':
        profile = UserProfile.objects.get(user=request.user)
        if profile.profile_picture:
            profile.profile_picture.delete(save=False)
            profile.profile_picture = None
            profile.save()
            messages.success(request, "Profile picture deleted successfully.")
        else:
            messages.error(request, "No profile picture to delete.")
    else:
        messages.error(request, "Invalid request method.")
    return redirect('profile')


@login_required
def update_profile(request):
    """Update user profile information including username,
    email, bio, location, and date of birth."""
    if request.method == 'POST':
        profile = UserProfile.objects.get(user=request.user)
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        profile.bio = request.POST.get('bio', profile.bio)
        profile.location = request.POST.get('location', profile.location)
        profile.date_of_birth = request.POST.get('date_of_birth')

        new_username = request.POST.get('username', user.username)

        if new_username and new_username != user.username:
            if new_username.isalnum():
                if not User.objects.filter(username=new_username).exists():
                    user.username = new_username
                    messages.success(
                        request, "Username updated successfully. \
                            You may need to log in again with your new \
                                username.")
                else:
                    messages.error(request, "Username is already taken.")
                    return redirect('profile')
            else:
                messages.error(request, "Username must be alphanumeric.")
                return redirect('profile')

        new_email = request.POST.get('email', user.email)
        current_email = user.email
        if new_email and new_email != current_email:
            user.email = new_email
            # Check if the email is already verified
            email_address = EmailAddress.objects.filter(
                user=user, email=new_email).first()
            if not email_address or not email_address.verified:
                # Send confirmation email if not verified
                send_email_confirmation(request, user, signup=False)
                messages.info(
                    request, "A confirmation email has been sent \
                    to your new email address.")
        else:
            user.email = current_email
        profile.save()
        user.save()
        messages.success(request, "Profile updated successfully.")
    else:
        messages.error(request, "Invalid request method.")
    return redirect('profile')


@login_required
def update_password(request):
    """Update the user's password."""
    if request.method == 'POST':
        user = request.user
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if user.check_password(current_password):
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(
                    request, "Password changed successfully.\
                        Please log in again.")
                logout(request)
                return redirect('account_login')
            else:
                messages.error(request, "New passwords do not match.")
        else:
            messages.error(request, "Current password is incorrect.")
    else:
        messages.error(request, "Invalid request method.")
    return redirect('profile')


def public_profile(request, userid):
    """Render a public profile page for a user."""
    try:
        user = User.objects.get(id=userid)
        profile = UserProfile.objects.get(user=user)
    except (User.DoesNotExist, UserProfile.DoesNotExist):
        messages.error(request, "User or profile not found.")
        return redirect('home')

    if profile.date_of_birth:
        today = date.today()
        age = today.year - profile.date_of_birth.year - (
            (today.month, today.day) < (
                profile.date_of_birth.month, profile.date_of_birth.day))
    else:
        age = None

    if profile.created_at:
        delta = now - profile.created_at
        years = delta.days // 365
        months = (delta.days % 365) // 30
        days = (delta.days % 365) % 30
        if years > 0:
            since_joined = f"{years} year{
                's' if years > 1 else ''} {
                    months} month{'s' if months > 1 else ''} {
                        days} day{'s' if days > 1 else ''} ago"
        elif months > 0:
            since_joined = f"{
                months} month{'s' if months > 1 else ''} {
                    days} day{'s' if days > 1 else ''} ago"
        else:
            since_joined = f"{
                days} day{'s' if days > 1 else ''} ago"
    else:
        since_joined = ""

    last_login = "Never logged in"
    if user.last_login:
        last_login_delta = now - user.last_login
        if last_login_delta.days > 30:
            last_login = "Last login more than 30 days ago"
        else:
            last_login = f"{last_login_delta.days} days ago"

    if profile.location:
        country = profile.location.split(
            ',')[-1].strip()
    else:
        country = "Country not specified"

    profile_data = {
        'profile_picture': (
            profile.profile_picture.url if profile.profile_picture else None
        ),
        'bio': profile.bio,
        'age': age,
        'since_joined': since_joined,
        'last_login': last_login,
        'country': country,
    }

    context = {
        'user': user,
        'profile': profile_data
    }
    return render(request, 'userprofile/public_profile.html', context=context)
