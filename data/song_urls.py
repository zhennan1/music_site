import os
import re

def find_and_save_urls_in_file(file_path, output_file):
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 正则表达式查找所有符合条件的URL
    pattern = r'href="(/n/ryqq/songDetail/[^\"]+)"'
    urls = re.findall(pattern, content)

    # 保存找到的URL到新文件中
    with open(output_file, 'a', encoding='utf-8') as file:
        for url in urls:
            file.write(url + '\n')

def process_folder(folder_path, output_file):
    # 遍历文件夹中的所有文件
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            find_and_save_urls_in_file(file_path, output_file)


folder_path = 'singer_info1'
output_file = 'song_urls1.txt'
process_folder(folder_path, output_file)

folder_path = 'singer_info2'
output_file = 'song_urls2.txt'
process_folder(folder_path, output_file)

folder_path = 'singer_info3'
output_file = 'song_urls3.txt'
process_folder(folder_path, output_file)

folder_path = 'singer_info4'
output_file = 'song_urls4.txt'
process_folder(folder_path, output_file)

folder_path = 'singer_info5'
output_file = 'song_urls5.txt'
process_folder(folder_path, output_file)
