from io import BytesIO
from django.http import HttpResponse
from django.db.models import Q
from collections import Counter
from PIL import Image, ImageDraw
import matplotlib
import os

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import jieba
import random
import numpy as np

# 字体路径
FONT_PATH = r'E:\My_project\Diary_project\diary\utils\simfang.ttf'


def get_font_properties():
    """获取字体属性"""
    if os.path.exists(FONT_PATH):
        return fm.FontProperties(fname=FONT_PATH)
    else:
        print(f"字体文件不存在: {FONT_PATH}")
        return None


def generate_wordcloud_image(request):
    """
    生成词云图片视图
    """
    try:
        # 获取字体属性
        font_prop = get_font_properties()

        # 1. 获取所有日记内容
        from Web.models import DiaryContents
        diaries = DiaryContents.objects.all()

        if not diaries.exists():
            return generate_default_wordcloud(font_prop)

        # 2. 合并所有内容并简单清理
        all_content = ""
        for diary in diaries:
            content = diary.content
            content = content.replace('#', '').replace('*', '').replace('`', '')
            content = content.replace('![', '').replace(']', '').replace('(', '')
            all_content += content + " "

        # 3. 分词和统计
        try:
            words = jieba.cut(all_content)
            word_list = [word for word in words if len(word) >= 2]
        except:
            word_list = [word for word in all_content.split() if len(word) >= 2]

        # 统计词频，只取前10个词
        if word_list:
            word_counter = Counter(word_list)
            top_words = word_counter.most_common(10)  # 只取前10个词
            word_freq = dict(top_words)
        else:
            word_freq = {}

        # 4. 生成词云图片
        img_buffer = BytesIO()
        plt.figure(figsize=(10, 8))

        if word_freq:
            generate_simple_wordcloud(plt, word_freq, font_prop)
        else:
            generate_empty_wordcloud(plt, font_prop)

        plt.axis('off')
        plt.tight_layout(pad=0)
        plt.savefig(img_buffer, format='PNG', dpi=100, bbox_inches='tight', pad_inches=0)
        plt.close()

        img_buffer.seek(0)
        return HttpResponse(img_buffer.getvalue(), content_type='image/png')

    except Exception as e:
        return generate_error_wordcloud(str(e), font_prop)


def generate_simple_wordcloud(plt, word_freq, font_prop=None):
    """
    简化版词云生成 - 更简单的布局算法
    """
    # 创建画布
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_facecolor('white')
    fig.patch.set_facecolor('white')

    if not word_freq:
        if font_prop:
            ax.text(0.5, 0.5, '暂无数据', ha='center', va='center', fontsize=30, fontproperties=font_prop)
        else:
            ax.text(0.5, 0.5, '暂无数据', ha='center', va='center', fontsize=30)
        return

    # 计算最大最小频率
    max_freq = max(word_freq.values())
    min_freq = min(word_freq.values())

    # 简化的网格布局 - 不再使用复杂的重叠检测
    words = list(word_freq.keys())
    frequencies = list(word_freq.values())

    # 计算每行显示几个词
    rows = min(3, len(words))  # 最多3行
    cols = (len(words) + rows - 1) // rows  # 计算需要的列数

    # 设置网格位置
    for i, (word, freq) in enumerate(word_freq.items()):
        # 计算字体大小
        if max_freq != min_freq:
            fontsize = 25 + (freq - min_freq) / (max_freq - min_freq) * 35
        else:
            fontsize = 40

        # 计算位置 - 使用简单的网格布局
        row = i // cols
        col = i % cols

        # 计算坐标
        x = 0.1 + col * (0.8 / max(1, cols - 1))
        y = 0.7 - row * (0.6 / max(1, rows - 1))

        # 随机颜色
        color = (random.random() * 0.7, random.random() * 0.7, random.random() * 0.7)

        # 轻微随机偏移，让布局看起来更自然
        x_offset = random.uniform(-0.05, 0.05)
        y_offset = random.uniform(-0.05, 0.05)

        # 绘制词语
        if font_prop:
            ax.text(x + x_offset, y + y_offset, word, fontsize=fontsize,
                    color=color, ha='center', va='center',
                    alpha=0.9, rotation=random.randint(-15, 15),
                    fontproperties=font_prop)
        else:
            ax.text(x + x_offset, y + y_offset, word, fontsize=fontsize,
                    color=color, ha='center', va='center',
                    alpha=0.9, rotation=random.randint(-15, 15))


def generate_empty_wordcloud(plt, font_prop=None):
    """生成空数据时的词云"""
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_facecolor('#f0f0f0')
    fig.patch.set_facecolor('#f0f0f0')

    if font_prop:
        ax.text(0.5, 0.5, '暂无日记数据\n开始写日记吧！',
                ha='center', va='center', fontsize=20,
                color='gray', linespacing=1.5,
                fontproperties=font_prop)
    else:
        ax.text(0.5, 0.5, '暂无日记数据\n开始写日记吧！',
                ha='center', va='center', fontsize=20,
                color='gray', linespacing=1.5)


def generate_error_wordcloud(error_msg, font_prop=None):
    """生成错误时的词云"""
    img_buffer = BytesIO()
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_facecolor('#fff0f0')
    fig.patch.set_facecolor('#fff0f0')

    if font_prop:
        ax.text(0.5, 0.5, f'生成词云失败\n{error_msg[:30]}...',
                ha='center', va='center', fontsize=16,
                color='red', linespacing=1.5,
                fontproperties=font_prop)
    else:
        ax.text(0.5, 0.5, f'生成词云失败\n{error_msg[:30]}...',
                ha='center', va='center', fontsize=16,
                color='red', linespacing=1.5)

    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.savefig(img_buffer, format='PNG', bbox_inches='tight', pad_inches=0)
    plt.close()
    img_buffer.seek(0)
    return HttpResponse(img_buffer.getvalue(), content_type='image/png')


def generate_default_wordcloud(font_prop=None):
    """生成默认词云"""
    img_buffer = BytesIO()
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_facecolor('#f0f8ff')
    fig.patch.set_facecolor('#f0f8ff')

    # 显示一些示例词语
    sample_words = ['日记', '心情', '回忆', '生活', '思考', '成长']
    for i, word in enumerate(sample_words):
        x = 0.2 + (i % 3) * 0.3
        y = 0.3 + (i // 3) * 0.3
        fontsize = 30 + i * 8  # 增大字体
        color = (0.2, 0.4, 0.6)

        if font_prop:
            ax.text(x, y, word, fontsize=fontsize, color=color,
                    ha='center', va='center', alpha=0.7,
                    fontproperties=font_prop)
        else:
            ax.text(x, y, word, fontsize=fontsize, color=color,
                    ha='center', va='center', alpha=0.7)

    if font_prop:
        ax.text(0.5, 0.8, '我的日记词云', fontsize=30,  # 增大标题字体
                ha='center', va='center', color='darkblue',
                fontproperties=font_prop)
    else:
        ax.text(0.5, 0.8, '我的日记词云', fontsize=30,
                ha='center', va='center', color='darkblue')

    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.savefig(img_buffer, format='PNG', bbox_inches='tight', pad_inches=0)
    plt.close()
    img_buffer.seek(0)
    return HttpResponse(img_buffer.getvalue(), content_type='image/png')