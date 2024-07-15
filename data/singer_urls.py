import re

def find_and_save_urls(input_file, output_file):
    # 读取文件内容
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # 正则表达式查找所有符合条件的URL
    pattern = r'href="(/n/ryqq/singer/[^\"]+)"'
    urls = re.findall(pattern, content)

    # 保存找到的URL到新文件中
    with open(output_file, 'w', encoding='utf-8') as file:
        for url in urls:
            file.write(url + '\n')

input_file = 'singer_list1.html'
output_file = 'singer_urls1.txt'
find_and_save_urls(input_file, output_file)

input_file = 'singer_list2.html'
output_file = 'singer_urls2.txt'
find_and_save_urls(input_file, output_file)

input_file = 'singer_list3.html'
output_file = 'singer_urls3.txt'
find_and_save_urls(input_file, output_file)

input_file = 'singer_list4.html'
output_file = 'singer_urls4.txt'
find_and_save_urls(input_file, output_file)

input_file = 'singer_list5.html'
output_file = 'singer_urls5.txt'
find_and_save_urls(input_file, output_file)
