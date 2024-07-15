import json
from django.core.management.base import BaseCommand
from music.models import Song, Singer

class Command(BaseCommand):
    help = 'Load data from JSON files'

    def handle(self, *args, **kwargs):
        with open('data/singer_info.json', encoding='utf-8') as f:
            singers_data = json.load(f)
            for singer_data in singers_data['singers']:
                singer, created = Singer.objects.get_or_create(
                    singer_id=singer_data['singer_id'],
                    defaults={
                        'singer_name': singer_data['singer_name'],
                        'image_url': singer_data['image_url'],
                        'bio': singer_data['bio'],
                        'original_url': singer_data['original_url'],
                    }
                )
                for song_data in singer_data['songs']:
                    if song_data.get('lyrics', '').strip():  # 检查歌词是否为空
                        Song.objects.get_or_create(
                            song_id=song_data['song_id'],
                            defaults={
                                'song_name': song_data['song_name'],
                                'singer': singer,
                                'image_url': song_data['image_url'],
                                'lyrics': song_data.get('lyrics', ''),
                                'original_url': song_data['original_url'],
                            }
                        )

        with open('data/song_info.json', encoding='utf-8') as f:
            songs_data = json.load(f)
            for song_data in songs_data['songs']:
                if song_data.get('lyrics', '').strip():  # 检查歌词是否为空
                    singer_name = song_data['singer_name']
                    singer_names = singer_name.split('/')
                    singers = []
                    for name in singer_names:
                        try:
                            singer = Singer.objects.get(singer_name=name.strip())
                            singers.append(singer)
                        except Singer.DoesNotExist:
                            print(f"Singer '{name.strip()}' does not exist in the database.")
                            continue

                    if singers:
                        for singer in singers:
                            song, created = Song.objects.get_or_create(
                                song_id=song_data['song_id'],
                                defaults={
                                    'song_name': song_data['song_name'],
                                    'singer': singer,
                                    'image_url': song_data['image_url'],
                                    'lyrics': song_data.get('lyrics', ''),  # 确保歌词被正确导入
                                    'original_url': song_data['original_url'],
                                }
                            )
                            # 更新已存在的歌曲歌词
                            if not created:
                                song.lyrics = song_data.get('lyrics', '')
                                song.save()
