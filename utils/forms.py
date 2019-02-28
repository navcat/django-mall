from django import forms

from utils.verify import VerifyCode


class VerifyCodeForm(forms.Form):
    """ 图片验证码"""

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._request = request

    verify_code = forms.CharField(label='验证码',
                                  max_length=4,
                                  widget=forms.TextInput(attrs={'placeholder': '请输入验证码'}),
                                  error_messages={'required': '请输入验证码'})

    def clean_verify_code(self):
        data = self.cleaned_data['verify_code']
        if self._request:
            code = VerifyCode(self._request)
            if not code.check(data):
                raise forms.ValidationError('验证码输入不正确')
        return data
