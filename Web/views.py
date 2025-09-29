from django.shortcuts import render, redirect
from Web.forms.account import RegisterModelForm, SendEmailForm, LoginForm
from Web.forms.notebook import DiaryContentForm
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt  # 免除认证
from Web import models
from django.db.models import Q  # 构造复杂查询


# Create your views here.
def index(request):
    user_id = request.session.get('user_id')
    notebook_obj = models.NoteBook.objects.filter(user_id=user_id)
    print(notebook_obj)
    return render(request, 'index.html', {'notebooks': notebook_obj})


@csrf_exempt
def register(request):
    if request.method == "GET":
        form = RegisterModelForm()
        return render(request, 'register.html', {'form': form})
    form = RegisterModelForm(request.POST)
    if form.is_valid():
        instance = form.save()
        models.NoteBook.objects.create(  # 用户注册时会初始化的偶默认笔记本
            user=instance,
            Book_Name=instance.username,
            description="开始你的第一本笔记吧"

        )

        return JsonResponse({'status': True, 'data': '/login/'})
    return JsonResponse({'status': False, 'error': form.errors})


def sendemail(request):
    if request.method == "GET":
        print(request.GET.get("email"))
        form = SendEmailForm(data=request.GET)
        if form.is_valid():
            # 发邮件并且写入Redis
            return JsonResponse({'status': True, })

        # form会帮助我们进行校验，所以就可以直接获取错误信息
        return JsonResponse({'status': False, 'error': form.errors})


def login(request):
    if request.method == "GET":
        form = LoginForm(request=request)
        return render(request, 'login.html', {'form': form})
    form = LoginForm(request, data=request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user_object = models.UserInfo.objects.filter(Q(email=username) | Q(username=username)).filter(
            password=password).first()  # 邮箱也可以实现登录
        if user_object:
            # 只有当用户名和密码存在正确时才允许跳转
            request.session['user_id'] = user_object.id
            request.session['username'] = user_object.username
            request.session.set_expiry(60 * 60 * 24 * 7)  # 用户登录成功后重写session数据为两周
            return redirect('/index/')
        form.add_error('username', '用户名或密码错误')
    return render(request, 'login.html', {'form': form})


def image_code(request):
    """图片验证码生成"""
    from utils.picture import generate_captcha
    from io import BytesIO

    img_object, code = generate_captcha()

    request.session['image_code'] = code  # 写入session
    request.session.set_expiry(60)  # 设置session的超时时间，不然默认是两周、

    stream = BytesIO()  # 图片写入内存
    img_object.save(stream, format='PNG')  # 图片写入内存

    stream.getvalue()  # 得到写入内存的图片
    print(code)
    return HttpResponse(stream.getvalue(), )  # 在得到内存中写入的数据后返回给前端


def logout(request):
    request.session.flush()  # 清空session数据
    return redirect('/login/')


def notebook_add(request):
    """添加笔记本"""
    notebook_obj = request.POST.get('notebook')
    content = request.POST.get('content')
    if notebook_obj and content:
        models.NoteBook.objects.create(user_id=request.session.get('user_id'), Book_Name=notebook_obj,
                                       description=content)
    return redirect('index')


def notebook_del(request, nid):
    """笔记本删除"""
    models.NoteBook.objects.filter(id=nid, user_id=request.session.get('user_id')).delete()
    return redirect('index')


def notebook_content_show(request, nid):
    """展示日记内容"""
    content_id = request.GET.get('content_id')

    content_obj = models.DiaryContents.objects.filter(id=content_id, notebook_id=nid).first()

    return render(request, 'content_show.html', {'nid': nid, 'content_obj': content_obj})


def notebook_content_add(request, nid):
    """日记内容添加"""
    if request.method == "GET":
        form = DiaryContentForm()
        return render(request, 'content_add.html', {'form': form})
    form = DiaryContentForm(request.POST)
    print(request.POST)
    if form.is_valid():
        diary_content = models.DiaryContents.objects.create(
            notebook_id=nid,
            title=form.cleaned_data['title'],
            content=form.cleaned_data['content'],
            weather=form.cleaned_data['weather']
        )
        print("success")
        return redirect('notebook_content_show', nid=nid)
    print(form.errors)
    return render(request, 'content_add.html', {'form': form})


def notebook_content_catalog(request, nid):
    """日记目录展示AJAX"""
    data = models.DiaryContents.objects.filter(notebook_id=nid).values('id', 'title', )
    return JsonResponse({'status': True, 'data': list(data)})


def notebook_content_del(request, nid, bid):
    print(nid)
    models.DiaryContents.objects.filter(id=nid, ).delete()
    return redirect('notebook_content_add', nid=bid)


def notebook_content_edit(request, nid, bid):
    """编辑文章"""
    if request.method == "GET":
        instance = models.DiaryContents.objects.filter(id=nid, ).first()
        form = DiaryContentForm(instance=instance)
        return render(request, 'content_edit.html', {'form': form, 'nid': nid})
    form = DiaryContentForm(request.POST, )
    if form.is_valid():
        print(form.cleaned_data)
        models.DiaryContents.objects.filter(id=nid, ).update(title=form.cleaned_data['title'],
                                                             content=form.cleaned_data['content'])
        return redirect('notebook_content_show', nid=bid)
