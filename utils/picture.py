import random
import string
from io import BytesIO
from django.http import HttpResponse
from django.core.cache import cache
from PIL import Image, ImageDraw, ImageFont, ImageFilter


def generate_captcha():
    # 验证码尺寸
    width, height = 120, 40

    # 创建图像
    image = Image.new('RGB', (width, height), (255, 255, 255))

    # 创建字体对象
    try:
        font = ImageFont.truetype('arial.ttf', 24)
    except IOError:
        font = ImageFont.load_default()

    # 创建绘制对象
    draw = ImageDraw.Draw(image)

    # 生成随机验证码（4位数字和字母）
    captcha_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    # 绘制验证码
    x = 10
    for char in captcha_chars:
        # 随机颜色
        color = (random.randint(0, 150), random.randint(0, 150), random.randint(0, 150))
        # 绘制字符
        draw.text((x, 10), char, font=font, fill=color)
        x += 25

    # 添加干扰线
    for i in range(5):
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=color, width=1)

    # 添加干扰点
    for i in range(100):
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.point((x, y), fill=color)


    img = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img, ''.join(captcha_chars)


if __name__ == '__main__':
    img_object, code = generate_captcha()

    # 图片写入本地文件
    # with open('code.png', 'wb') as f:
    #     img_object.save(f,format='PNG')
    #
    # # 写入内存
    # from io import BytesIO
    # stream = BytesIO()
    # img_object.save(stream, format='PNG')
    #
    # # 得到写入内存的图片
    # stream.getvalue()
