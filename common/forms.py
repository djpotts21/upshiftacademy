'''
Custom forms for user authentication using Django Allauth.
This module contains custom forms for login, signup, password reset,
and password reset key handling, enhancing the user experience with
customized widgets and attributes.
'''

from allauth.account.forms import (
    LoginForm,
    ResetPasswordForm,
    SignupForm,
    ResetPasswordKeyForm
)


class CustomLoginForm(LoginForm):
    """
    Custom login form to enhance user experience with custom widgets.
    This form modifies the default login form to include custom
    attributes for the login and password fields.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customize the 'login' field (username/email)
        self.fields['login'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username or email',
        })

        # Customize the 'password' field
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password',
        })

        # Optionally, you can set the 'autocomplete' attribute
        self.fields['login'].widget.attrs['autocomplete'] = 'username'
        self.fields['password'].widget.attrs[
            'autocomplete'
            ] = 'current-password'

        # Optionally remove labels if you prefer placeholders only
        self.fields['login'].label = ''
        self.fields['password'].label = ''


class CustomResetPasswordForm(ResetPasswordForm):
    """Custom reset password form to enhance user experience
    with custom widgets. This form modifies the default reset
    password form to include custom attributes for the email
    field.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customize the 'email' field
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Email address',
        })

        # Optionally, you can set the 'autocomplete' attribute
        self.fields['email'].widget.attrs['autocomplete'] = 'email'

        # Optionally remove labels if you prefer placeholders only
        self.fields['email'].label = ''


class CustomSignupForm(SignupForm):
    """
    Custom signup form to enhance user experience with custom widgets.
    This form modifies the default signup form to include custom
    attributes for the username, email, and password fields.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customize the 'username' field
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username',
        })

        # Customize the 'email' field
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Email address',
        })

        # Customize the 'password1' field
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password',
        })

        # Customize the 'password2' field
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm Password',
        })

        # Optionally set autocomplete attributes
        self.fields['username'].widget.attrs['autocomplete'] = 'username'
        self.fields['email'].widget.attrs['autocomplete'] = 'email'
        self.fields['password1'].widget.attrs['autocomplete'] = 'new-password'
        self.fields['password2'].widget.attrs['autocomplete'] = 'new-password'

        # Optionally remove labels if you prefer placeholders only
        self.fields['username'].label = ''
        self.fields['email'].label = ''
        self.fields['password1'].label = ''
        self.fields['password2'].label = ''


class CustomResetPasswordKeyForm(ResetPasswordKeyForm):
    """
    Custom reset password key form to enhance user experience
    with custom widgets. This form modifies the default reset
    password key form to include custom attributes for the
    password fields.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, placeholder in {
            'password1': 'New Password',
            'password2': 'Confirm New Password'
        }.items():
            if field_name in self.fields:
                field = self.fields[field_name]
                field.widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': placeholder,
                    'autocomplete': 'new-password'
                })
                field.label = ''  # optional: hide label if using placeholders
