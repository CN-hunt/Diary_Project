from django.db import models


# Create your models here.

class UserInfo(models.Model):
    """用户表"""
    username = models.CharField(verbose_name='用户名', max_length=50)
    email = models.EmailField(verbose_name='邮箱', max_length=50)
    password = models.CharField(verbose_name='密码', max_length=50)


class NoteBook(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    Book_Name = models.CharField(verbose_name='日记本名称',max_length=50)
    description = models.CharField(verbose_name='描述', max_length=50)
    COLOR_CHOICES = (
        (1, '#A7CE4F'),
        (2, '#E7DA96'),
        (3, '#9EBAC6'),
        (4, '#F79A57'),
        (5, '#EB4A59'),
        (6, '#5E595A'),
        (7, '#BA55D3'),
    )
    cover_color = models.SmallIntegerField(verbose_name='封面颜色', choices=COLOR_CHOICES,default=1)
    created_at = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)


class DiaryContents(models.Model):
    """内容表"""
    notebook = models.ForeignKey(NoteBook, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='标题', max_length=50)
    content = models.TextField(verbose_name='日记内容')
    weather_choice = (
        ('1', '☀️ 晴天'),
        ('2', '☁️ 多云'),
        ('3', '🌧️ 雨天'),
        ('4', '❄️ 雪天'),
        ('5', '💨 大风'),
        ('6', '🌫️ 雾天'),
        ('7', '⛈️ 雷雨'),
        ('8', '🌤️ 一般'),
    )
    weather = models.SmallIntegerField(verbose_name='天气', choices=weather_choice)
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
