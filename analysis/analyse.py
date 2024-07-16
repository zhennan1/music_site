import json
import jieba
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
from matplotlib import font_manager

# 文件列表，更新文件路径
singer_files = [f'../data/singer_info{i}.json' for i in range(1, 6)] + ['../data/singer_info.json']
song_files = [f'../data/song_info{i}.json' for i in range(1, 6)] + ['../data/song_info.json']

font_path = '/mnt/c/Windows/Fonts/simsun.ttc'  # 确保此路径正确

# 设置matplotlib使用simsun字体
simsun_font = font_manager.FontProperties(fname=font_path)

all_lyrics_lengths = []
all_fan_counts = []

# 首先遍历所有文件，找到全局最小值和最大值
for singer_file, song_file in zip(singer_files, song_files):
    with open(song_file, 'r', encoding='utf-8') as f:
        songs_data = json.load(f)
        all_lyrics_lengths.extend([len(song['lyrics']) for song in songs_data['songs'] if len(song['lyrics']) > 0])
    
    with open(singer_file, 'r', encoding='utf-8') as f:
        singers_data = json.load(f)
        for singer in singers_data['singers']:
            fans = singer['fans']
            if '万' in fans:
                all_fan_counts.append(float(fans.replace('万', '')) * 10000)
            else:
                all_fan_counts.append(float(fans))

# 找到全局最小值和最大值
lyrics_length_min, lyrics_length_max = min(all_lyrics_lengths), max(all_lyrics_lengths)
fan_count_min, fan_count_max = min(all_fan_counts), max(all_fan_counts)

def process_files(singer_file, song_file):
    # 提取歌词文本和歌手粉丝数量
    lyrics_text = ""
    fan_counts = []

    # 读取歌曲文件并提取歌词
    with open(song_file, 'r', encoding='utf-8') as f:
        songs_data = json.load(f)
        for song in songs_data['songs']:
            if len(song['lyrics']) > 0:
                lyrics_text += song['lyrics']

    # 读取歌手文件并提取粉丝数量
    with open(singer_file, 'r', encoding='utf-8') as f:
        singers_data = json.load(f)
        for singer in singers_data['singers']:
            fans = singer['fans']
            if '万' in fans:
                fan_counts.append(float(fans.replace('万', '')) * 10000)
            else:
                fan_counts.append(float(fans))

    # 歌词热词统计
    words = jieba.lcut(lyrics_text)
    stopwords = set([
        '的', '了', '和', '是', '都', '也', '就', '而', '及', '与', '着', '啊', '我',  # 中文停用词
        'the', 'a', 'an', 'is', 'are', 'and', 'of', 'to', 'in', 'that', 'it', 'for', 'on', 'with', 'as', 'was', 'but', 'by', 'at', 'or', 'from'  # 英文停用词
    ])
    word_counts = Counter(word for word in words if word.lower() not in stopwords and len(word) > 1)
    common_words = word_counts.most_common(20)

    # 生成词云图
    wordcloud = WordCloud(font_path=font_path, width=800, height=400, background_color='white').generate_from_frequencies(word_counts)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Lyrics Word Cloud', fontproperties=simsun_font)
    plt.savefig(f'wordcloud_{singer_file.split("/")[-1].split(".")[0]}.png')
    plt.close()

    # 歌词长度分布
    lyrics_lengths = [len(song['lyrics']) for song in songs_data['songs'] if len(song['lyrics']) > 0]
    plt.figure(figsize=(10, 5))
    plt.hist(lyrics_lengths, bins=20, range=(lyrics_length_min, lyrics_length_max), edgecolor='black')
    plt.title('Lyrics Length Distribution', fontproperties=simsun_font)
    plt.xlabel('Lyrics Length', fontproperties=simsun_font)
    plt.ylabel('Number of Songs', fontproperties=simsun_font)
    plt.savefig(f'lyrics_length_distribution_{song_file.split("/")[-1].split(".")[0]}.png')
    plt.close()

    # 歌手粉丝数量分布
    plt.figure(figsize=(10, 5))
    plt.hist(fan_counts, bins=20, range=(fan_count_min, fan_count_max), edgecolor='black')
    plt.title('Singer Fan Count Distribution', fontproperties=simsun_font)
    plt.xlabel('Fan Count', fontproperties=simsun_font)
    plt.ylabel('Number of Singers', fontproperties=simsun_font)
    plt.savefig(f'singer_fan_count_distribution_{singer_file.split("/")[-1].split(".")[0]}.png')
    plt.close()

    # 将热词统计保存到Excel
    word_df = pd.DataFrame(common_words, columns=['Word', 'Frequency'])
    word_df.to_excel(f'word_frequency_{song_file.split("/")[-1].split(".")[0]}.xlsx', index=False)

    # 将歌词长度保存到Excel
    length_df = pd.DataFrame(lyrics_lengths, columns=['Lyrics Length'])
    length_df.to_excel(f'lyrics_length_{song_file.split("/")[-1].split(".")[0]}.xlsx', index=False)

    # 将粉丝数量保存到Excel
    fan_df = pd.DataFrame(fan_counts, columns=['Fan Count'])
    fan_df.to_excel(f'fan_count_{singer_file.split("/")[-1].split(".")[0]}.xlsx', index=False)

# 对每个文件进行处理
for singer_file, song_file in zip(singer_files, song_files):
    process_files(singer_file, song_file)
