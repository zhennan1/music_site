import json

def load_json(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_json(data, file_name):
    with open(file_name, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

def update_singer_info_with_song_images(singer_info, song_info):
    song_images = {song["song_id"]: song["image_url"] for song in song_info["songs"]}

    for singer in singer_info["singers"]:
        for song in singer["songs"]:
            song_id = song["song_id"]
            if song_id in song_images:
                song["image_url"] = song_images[song_id]
    
    return singer_info

def main():
    singer_info_file = 'singer_info_1-3.json'
    song_info_file = 'song_info_1-3.json'
    
    singer_info = load_json(singer_info_file)
    song_info = load_json(song_info_file)
    
    updated_singer_info = update_singer_info_with_song_images(singer_info, song_info)
    
    save_json(updated_singer_info, singer_info_file)

if __name__ == "__main__":
    main()
