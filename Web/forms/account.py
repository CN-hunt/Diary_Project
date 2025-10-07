import hashlib
from django.conf import settings
from django import forms
from Web import models
from Web.models import UserInfo
from django.core.exceptions import ValidationError
import random
from django.core.validators import RegexValidator
from django.core.mail import send_mail
from django_redis import get_redis_connection
from django.utils.translation import gettext_lazy as _
import os


def md5(string):
    """md5加密"""
    hash_object = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    hash_object.update(string.encode('utf-8'))
    return hash_object.hexdigest()


class RegisterModelForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '密码'}),
        min_length=8,  # 最小长度8位
        max_length=20,  # 最大长度20位
        error_messages={
            'min_length': _('密码长度不能少于8个字符'),
            'max_length': _('密码长度不能超过20个字符'),
        }
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('确认密码')})
    )
    code = forms.CharField(label=_('验证码'),
                           widget=forms.TextInput(
                               attrs={'class': 'form-control', 'placeholder': _('请输入验证码'), 'name': 'confirm'}))

    class Meta:
        model = models.UserInfo
        fields = ('username', 'email', 'password', 'confirm_password', 'code')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('用户名')}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('邮箱')}),
            # 注意：此处不再重复定义password的widget，已在上方显式字段中定义
        }

    def clean_username(self):
        """限制用户名重复"""
        username = self.cleaned_data['username']  # 获取用户名的值
        exists = model = UserInfo.objects.filter(username=username).exists()
        if exists:
            raise ValidationError(_("用户名已经存在"))

        return username

    def clean_email(self):
        """限制邮箱唯一性"""
        email = self.cleaned_data['email']  # 获取邮箱
        exists = model = UserInfo.objects.filter(email=email).exists()
        if exists:
            raise ValidationError(_("邮箱已经存在"))
        return email

    def clean_password(self):
        """加密密码"""
        password = self.cleaned_data['password']
        # 加密后返回
        return md5(password)

    def clean_confirm_password(self):
        """密码和确认密码的对比"""
        pwd = self.cleaned_data.get('password')  # 获取输入的密码
        confirm_pwd = md5(self.cleaned_data.get('confirm_password'))  # 获取输入的确认密码，这里也需要加密，不然一个密文一个明文无法校验通过
        print(pwd)
        print(confirm_pwd)
        if pwd != confirm_pwd:
            raise ValidationError(_("两次密码不一致"))
        return confirm_pwd

    def clean_code(self):
        """验证码确认"""
        code = self.cleaned_data['code']
        # email = self.cleaned_data['email']  # 跟据邮箱找到对应Redis里面的值，之前已经存储成功了，bug修改：get
        email = self.cleaned_data.get('email')
        if not email:
            return code
        conn = get_redis_connection()
        redis_code = conn.get(email)
        if not redis_code:
            raise ValidationError(_("验证码失效或未发送"))
        redis_str_code = redis_code.decode('utf-8')  # Redis里面存的是字节文件所以需要转化一下才能用
        if code != redis_str_code:  # .strip()的作用是将用户输入的空格去掉
            raise ValidationError(_("验证码错误请重新输入"))


class SendEmailForm(forms.Form):
    """邮箱及其验证"""
    email = forms.EmailField(label=_('邮箱'),
                             validators=[RegexValidator(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
                                                        "邮箱格式错误")])

    def clean_email(self):
        """邮箱存在校验钩子方法"""
        email = self.cleaned_data['email']

        # 校验数据库中是否已经存在邮箱
        exists = models.UserInfo.objects.filter(email=email).exists()
        if exists:
            raise ValidationError(_("邮箱已存在"))

        # 发邮件 & 写入 Redis

        # 邮件发送
        code = random.randrange(1000, 9999)  # 生成随机码
        subject = _('邮箱验证码')  # 邮件标题
        from_email = settings.EMAIL_HOST_USER  # 发送方
        to = email  # 接收方
        text_content = _('您好这是您的邮箱验证码:') + str(code)  # 邮件内容
        print(from_email)
        res = send_mail(subject, text_content, from_email, [to], )
        print(res)
        if res != 1:
            raise ValidationError(_("发送失败，请检查"))

        conn = get_redis_connection()  # 获取Redis连接
        conn.set(email, code, ex=600)  # KEY是邮箱，value是验证码

        return email


class LoginForm(forms.Form):
    username = forms.CharField(label=_('用户名或邮箱'), widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label=_('密码'),
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}, render_value=True))
    picture_code = forms.CharField(label=_('图片验证码'), widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_password(self):
        """加密密码"""
        password = self.cleaned_data['password']
        # 加密后返回
        return md5(password)

    def clean_picture_code(self):
        """校验图片验证码是否正确"""
        # 读取用户输入的验证码
        code = self.cleaned_data['picture_code']
        session_code = self.request.session.get('image_code')  # 得到session中的code
        if not session_code:
            raise ValidationError(_('验证码已过期，请再次获取'))

        if code != session_code:
            raise ValidationError(_("验证码输入错误"))

        return code
