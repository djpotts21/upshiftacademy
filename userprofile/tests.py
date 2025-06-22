'''
Unit tests for the UserProfile app in a Django project.
This module contains tests for the UserProfile app, including profile views,
image uploads, and profile updates.
'''
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from userprofile.models import UserProfile

# pylint: disable=no-member

valid_image = SimpleUploadedFile(
    "test.png",
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR",
    content_type="image/png"
)


class UserProfileTests(TestCase):
    """Tests for the UserProfile app."""
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='pass123')
        self.profile = UserProfile.objects.create(
            user=self.user,
            bio='This is a test bio',
            location='Test Location',
            date_of_birth='2000-01-01'
        )
        self.client.login(username='testuser', password='pass123')

    def test_profile_view_authenticated(self):
        """Test the profile view for authenticated users."""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'userprofile/profile.html')

    def test_profile_view_unauthenticated(self):
        """Test the profile view for unauthenticated users."""
        self.client.logout()
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_upload_profile_picture_success(self):
        """Test uploading a profile picture successfully."""
        response = self.client.post(reverse(
            'upload_profile_picture'), {'profile_picture': valid_image})
        self.assertRedirects(response, reverse('profile'))
        self.profile.refresh_from_db()
        self.assertTrue(self.profile.profile_picture)

    def test_upload_profile_picture_failure(self):
        """Test uploading a profile picture with no file."""
        response = self.client.post(reverse(
            'upload_profile_picture'), {})
        self.assertRedirects(response, reverse('profile'))

    def test_upload_images_success(self):
        """Test uploading images successfully."""
        response = self.client.post(
            reverse('upload_images'), {'file': valid_image})
        self.assertRedirects(response, reverse('profile'))
        self.assertEqual(self.profile.uploaded_images.count(), 1)

    def test_delete_image_success(self):
        """Test deleting an uploaded image successfully."""
        image = self.profile.uploaded_images.create(file=valid_image)
        response = self.client.post(reverse('delete_image', args=[image.id]))
        self.assertRedirects(response, reverse('profile'))
        self.assertEqual(self.profile.uploaded_images.count(), 0)

    def test_delete_image_not_found(self):
        """Test deleting an image that does not exist."""
        response = self.client.post(reverse('delete_image', args=[999]))
        self.assertRedirects(response, reverse('profile'))

    def test_delete_profile_picture_success(self):
        """Test deleting the profile picture successfully."""
        self.profile.profile_picture = valid_image
        self.profile.save()
        response = self.client.post(reverse('delete_profile_picture'))
        self.assertRedirects(response, reverse('profile'))
        self.profile.refresh_from_db()
        self.assertFalse(self.profile.profile_picture)

    def test_update_profile_success(self):
        """Test updating the user profile successfully."""
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'bio': 'Hello world',
            'location': 'London',
            'username': 'newtestuser',
            'email': 'test@example.com',
            'date_of_birth': '1990-01-01'
        }
        response = self.client.post(reverse('update_profile'), data)
        self.assertRedirects(response, reverse('profile'))
        self.user.refresh_from_db()
        self.profile.refresh_from_db()
        self.assertEqual(self.user.username, 'newtestuser')
        self.assertEqual(self.profile.bio, 'Hello world')

    def test_update_profile_username_taken(self):
        """Test updating the profile with a username that is already taken."""
        User.objects.create_user(username='existinguser', password='123')
        data = {'username': 'existinguser'}
        response = self.client.post(reverse('update_profile'), data)
        self.assertRedirects(response, reverse('profile'))
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.username, 'existinguser')

    def test_update_profile_invalid_method(self):
        """Test accessing the update profile view with an invalid method."""
        response = self.client.get(reverse('update_profile'))
        self.assertRedirects(response, reverse('profile'))
