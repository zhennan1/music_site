import os
import re
import json

def extract_singer_info(file_content):
    # 提取歌手名称
    name_match = re.search(r'<title>(.*?) - QQ音乐', file_content)
    name = name_match.group(1).strip() if name_match else ""
    
    # 提取歌手图片URL
    image_url_match = re.search(r'"pic":"http:\\u002F\\u002Fy.gtimg.cn\\u002Fmusic\\u002Fphoto_new\\u002F([^"]+)"', file_content)
    image_url = "http://y.gtimg.cn/music/photo_new/" + image_url_match.group(1) if image_url_match else ""
    
    # 提取歌手简介
    bio_match = re.search(r'<h3 class="popup_data_detail__tit">歌手简介</h3>(.*?)</div><i class="popup_data_detail__arrow">', file_content, re.S)
    bio = bio_match.group(1).strip() if bio_match else ""
    
    # 提取歌曲信息
    songs = []
    for song_match in re.findall(r'href="/n/ryqq/songDetail/(\w+)">([^<]+)</a>', file_content):
        song_id, song_name = song_match
        song_original_url = f"https://y.qq.com/n/ryqq/songDetail/{song_id}"
        songs.append({
            "song_id": song_id,
            "song_name": song_name,
            "original_url": song_original_url
        })
    
    return name, image_url, bio, songs

def process_folder(folder_path):
    singers = []
    
    for filename in os.listdir(folder_path):
        if filename.endswith('.html'):
            singer_id = filename.replace('.html', '')
            file_path = os.path.join(folder_path, filename)
            
            with open(file_path, 'r', encoding='utf-8') as file:
                file_content = file.read()
            
            name, image_url, bio, songs = extract_singer_info(file_content)
            original_url = f"https://y.qq.com/n/ryqq/singer/{singer_id}"
            
            singer_info = {
                "singer_id": singer_id,
                "singer_name": name,
                "image_url": image_url,
                "bio": bio,
                "original_url": original_url,
                "songs": songs
            }
            
            singers.append(singer_info)
    
    return singers

def save_json(data, file_name):
    with open(file_name, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

def main():
    folder_names = [f'singer_info{i}' for i in range(1, 6)]
    all_singers = []
    
    for folder_name in folder_names:
        singers = process_folder(folder_name)
        all_singers.extend(singers)
        save_json({"singers": singers}, f'{folder_name}.json')
    
    save_json({"singers": all_singers}, 'singer_info.json')
    save_json({"singers": all_singers[:sum([len(process_folder(f'singer_info{i}')) for i in range(1, 4)])]}, 'singer_info_1-3.json')

if __name__ == "__main__":
    main()
