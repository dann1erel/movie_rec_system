import yt_dlp
import pandas as pd
import os

def download_youtube_shorts(movie_name, num_videos):
    ydl_opts = {
        'format': 'best',  # Выбираем лучшее доступное видео с аудио в одном потоке
        'outtmpl': os.path.join(f'C:\movie_rec_system\clips\{movie_name}', '%(title)s.%(ext)s'),  # Указываем путь для скачивания
        'playlistend': num_videos,  # Ограничиваем количество видео
        'writedescription': True,  # Сохраняем описание видео
    }

    # with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    #     ydl.download([channel_url])
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            search_query = f"ytsearch{num_videos}: {movie_name} shorts"
            info = ydl.extract_info(search_query, download=False)

            video_count = 0
            for entry in info['entries']:
                if video_count >= num_videos:
                    break

                video_url = entry['webpage_url']
                ydl.download([video_url])

                video_count += 1

        except Exception as e:
            print(f"Ошибка при скачивании: {str(e)}")

if __name__ == "__main__":
    df = pd.read_csv('C:\movie_rec_system\data\kinopoisk-top250.csv')
    for movie_name in df['movie'][:5]:
        num_videos = 3
        download_youtube_shorts(movie_name, num_videos)
