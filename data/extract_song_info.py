import os
import re
import json

def extract_song_info(file_content):
    # 提取歌曲名称和歌手名称
    title_match = re.search(r'<title>(.*?) - (.*?) - QQ音乐', file_content)
    if title_match:
        song_name = title_match.group(1).strip()
        singer_name = title_match.group(2).strip()
    else:
        song_name = ""
        singer_name = ""
    
    # 提取歌曲图片URL
    image_url_match = re.search(r'"picurl":"\\u002F\\u002Fy.qq.com\\u002Fmusic\\u002Fphoto_new\\u002F([^?]+)\?max_age=2592000"', file_content)
    image_url = "https://y.qq.com/music/photo_new/" + image_url_match.group(1) if image_url_match else ""
    
    lyrics = ""
    
    return song_name, singer_name, image_url, lyrics

def get_lyrics(lyrics_folder, singer_name, song_name):
    lyrics_content = ""
    for lyrics_file in os.listdir(lyrics_folder):
        if lyrics_file.endswith('.txt') and (singer_name in lyrics_file or lyrics_file.replace('_歌词.txt', '') in singer_name):
            file_path = os.path.join(lyrics_folder, lyrics_file)
            with open(file_path, 'r', encoding='utf-8') as file:
                file_lyrics_content = file.read()
                
                song_lyrics_match = re.search(rf'{re.escape(song_name)} - .*?\n(.*?)\n----------------------------------------------', file_lyrics_content, re.S)
                if song_lyrics_match:
                    lyrics_content = song_lyrics_match.group(1).strip()
                    break
    return lyrics_content

def process_folder(folder_path, lyrics_folder):
    songs = []
    
    for filename in os.listdir(folder_path):
        if filename.endswith('.html'):
            song_id = filename.replace('.html', '')
            file_path = os.path.join(folder_path, filename)
            
            with open(file_path, 'r', encoding='utf-8') as file:
                file_content = file.read()
            
            song_name, singer_name, image_url, _ = extract_song_info(file_content)
            lyrics = get_lyrics(lyrics_folder, singer_name, song_name)
            original_url = f"https://y.qq.com/n/ryqq/songDetail/{song_id}"
            
            song_info = {
                "song_id": song_id,
                "song_name": song_name,
                "singer_name": singer_name,
                "image_url": image_url,
                "lyrics": lyrics,
                "original_url": original_url
            }
            
            songs.append(song_info)
    
    return songs

def save_json(data, file_name):
    with open(file_name, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

def main():
    folder_names = [f'song_info{i}' for i in range(1, 6)]
    all_songs = []
    songs_1_to_3 = []
    
    lyrics_folder = './lyrics'
    
    for i, folder_name in enumerate(folder_names, 1):
        songs = process_folder(folder_name, lyrics_folder)
        all_songs.extend(songs)
        save_json({"songs": songs}, f'{folder_name}.json')
        if i <= 3:
            songs_1_to_3.extend(songs)
    
    save_json({"songs": all_songs}, 'song_info.json')
    save_json({"songs": songs_1_to_3}, 'song_info_1-3.json')

if __name__ == "__main__":
    main()
