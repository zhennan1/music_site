import requests
import re
from collections import defaultdict

URL = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp?"

headers = {
    "origin": "https://y.qq.com",
    "referer": "https://y.qq.com/n/yqq/song/004Z8Ihr0JIu5s.html",
    "user-agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
}

params = {
    "ct": "24",
    "qqmusic_ver": "1298",
    "remoteplace": "txt.yqq.lyric",
    "searchid": "103347689276433275",
    "aggr": "0",
    "catZhida": "1",
    "lossless": "0",
    "sem": "1",
    "t": "7",
    "p": "1",
    "n": "5",
    "w": "",
    "g_tk_new_20200303": "5381",
    "g_tk": "5381",
    "loginUin": "0",
    "hostUin": "0",
    "format": "json",
    "inCharset": "utf8",
    "outCharset": "utf-8",
    "notice": "0",
    "platform": "yqq.json",
    "needNewCode": "0",
}

def fetch_lyrics_for_singer(singer):
    params["w"] = singer
    album_dic = defaultdict(list)

    def check(songname, albumname):
        if singer not in songname or "-" not in songname:
            return False

        if albumname in album_dic:
            for song in album_dic[albumname]:
                if songname in song[0]:
                    return False
        return True

    for p in range(1, 100):
        params["p"] = p
        res = requests.get(URL, headers=headers, params=params).json()
        list_lyric = res["data"]["lyric"]["list"]
        if len(list_lyric) == 0:
            counts = 0
            for albumname in album_dic.keys():
                counts += len(album_dic[albumname])
            break
        for lyric in list_lyric:
            content = re.sub(r"\\n ", "\n", lyric["content"]).strip()
            songname = content.split("\n")[0].strip()
            albumname = lyric["albumname"].strip()
            if check(songname, albumname):
                if len(albumname) == 0:
                    albumname = "其它"
                album_dic[albumname].append((songname, content))
                print(albumname + "\n  " + songname)

    album_list = sorted(album_dic.items(), key=lambda d: len(d[1]), reverse=True)

    with open(f"lyrics/{singer}_歌词.txt", "w", encoding='utf-8') as f_lyric:
        for album in album_list:
            for song in album[1]:
                f_lyric.write(song[1])
                f_lyric.write("\n----------------------------------------------\n")

def main():
    for i in range(1, 6):
        input_file = f'singer_name_list{i}.txt'
        
        with open(input_file, 'r', encoding='utf-8') as file:
            singers = file.readlines()
            singers = [singer.strip() for singer in singers]
        
        for singer in singers:
            print(f"Fetching lyrics for {singer} from {input_file}...")
            fetch_lyrics_for_singer(singer)
            print(f"Finished fetching lyrics for {singer} from {input_file}.")

if __name__ == "__main__":
    main()
