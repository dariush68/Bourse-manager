from django import forms
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from bourseapp.models import *


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='اختیاری.', label='نام')
    last_name = forms.CharField(max_length=30, required=False, help_text='اختیاری.', label='نام خانوادگی')
    email = forms.EmailField(max_length=254, required=False, help_text='اختیاری', label='ایمیل')
    password1 = forms.CharField(
        label="رمز عبور",
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="تکرار رمز عبور",
        strip=False,
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)
        labels = {
            'username': 'نام کاربری',
        }


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = '__all__'
        exclude = ["user", "category", "company"]
        labels = {
            'title': 'عنوان',
            'tag': 'تگ',
            'description': 'توضیحات',
            'reference': 'آدرس مرجع',
            'isSuperUserPermition': 'دسترسی سطح بالا'
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(NewsForm, self).__init__(*args, **kwargs)
        self.fields['createAt'] = JalaliDateField(label='تاریخ',  # date format is  "yyyy-mm-dd"
                                                  widget=AdminJalaliDateWidget  # optional, to use default datepicker
                                                  )

        if self.user.is_superuser:
            pass
        else:
            self.fields['isSuperUserPermition'].widget.attrs['disabled'] = True
            self.fields['isSuperUserPermition'].label = ""


