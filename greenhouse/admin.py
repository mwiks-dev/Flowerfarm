from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import Production, User

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

def send_invitation_email(modeladmin, request, queryset):
    for user in queryset:
        # Generate an invitation token for each user
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Create the invitation link
        invitation_link = request.build_absolute_uri(
            reverse('activate_account', args=[uid, token])
        )

        # Compose and send the invitation email
        subject = 'Invitation to Join Our Platform'
        message = f"Click the following link to join our platform: {invitation_link}"
        sender = 'mwiksdev@gmail.com'
        recipient_list = [user.email]
        send_mail(subject, message, sender, recipient_list,  fail_silently=False)

send_invitation_email.short_description = 'Send Invitation Email'

# Register your models here.
admin.site.register(Production)

class UserCreationForm(forms.ModelForm):
    #A form for creating new users. Includes all the required
    #fields, plus a repeated password.
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email','full_name','staff_number')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
class UserChangeForm(forms.ModelForm):
#A form for updating users. Includes all the fields on
#the user, but replaces the password field with admin's
#password hash display field.

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'full_name','staff_number','password', 'is_active','is_staff')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
    
class UserAdmin(BaseUserAdmin):
    actions = [send_invitation_email]
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'full_name','staff_number','is_active', 'is_staff')
    list_filter = ('email',)
    fieldsets = (
        (None, {'fields': ('full_name','email', 'password','staff_number')}),
        ('Permissions', {'fields': ('is_staff',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)