"""forms.py
Defines the form for submitting code in a code challenge."""
from django import forms


class CodeSubmissionForm(forms.Form):
    """Form for submitting code in a code challenge."""
    code = forms.CharField(
        label="Your Code",
        widget=forms.Textarea(attrs={
            'rows': 15,
            'class': 'form-control',
            'placeholder': 'Type your code here...'
        })
    )
