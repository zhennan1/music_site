import os
import re

def extract_first_h1_content(file_path):
    """Extracts the content of the first <h1 class="data__name_txt">...</h1> from a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        match = re.search(r'<h1 class="data__name_txt">(.*?)</h1>', content)
        if match:
            return match.group(1)
    return None

def process_files_in_directory(directory):
    """Processes all files in the given directory to extract content from <h1 class="data__name_txt">...</h1> tags."""
    extracted_contents = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            content = extract_first_h1_content(file_path)
            if content:
                extracted_contents.append(content)
    return extracted_contents

def save_contents_to_file(contents, output_file):
    """Saves the extracted contents to a specified output file, one per line."""
    with open(output_file, 'w', encoding='utf-8') as file:
        for content in contents:
            file.write(content + '\n')


directory = 'singer_info1'
output_file = 'singer_name_list1.txt'
contents = process_files_in_directory(directory)
save_contents_to_file(contents, output_file)

directory = 'singer_info2'
output_file = 'singer_name_list2.txt'
contents = process_files_in_directory(directory)
save_contents_to_file(contents, output_file)

directory = 'singer_info3'
output_file = 'singer_name_list3.txt'
contents = process_files_in_directory(directory)
save_contents_to_file(contents, output_file)

directory = 'singer_info4'
output_file = 'singer_name_list4.txt'
contents = process_files_in_directory(directory)
save_contents_to_file(contents, output_file)

directory = 'singer_info5'
output_file = 'singer_name_list5.txt'
contents = process_files_in_directory(directory)
save_contents_to_file(contents, output_file)