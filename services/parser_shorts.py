import yt_dlp
import os
from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.editor import vfx, afx
from movies import Movies
import sys
import threading


class QuietLogger:
    def debug(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): print(msg)  # Можно показывать только ошибки


# скачать трейлер с ютуб
def download_trailer(data_dict, url, mode):
    # Путь к файлу
    output_path = os.path.join('./services/clips', f'{data_dict["id"]}.mp4')

    # Параметры yt-dlp
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': output_path,
        'merge_output_format': 'mp4',
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
        'logger': QuietLogger(),
        'quiet': True,
        'no_warnings': True,
        'cookiefile': './data/www.youtube.com_cookies.txt'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            if mode == 'not_url':
                # Сформировать поисковый запрос по TikTok
                search_query = f"ytsearch1:{data_dict['name_rus']} {data_dict['movie_year']} трейлер"
                # print(f"Поиск: {search_query}")

                info = ydl.extract_info(search_query, download=False)
                if info['entries']:
                    video_url = info['entries'][0]['webpage_url']
                    ydl.download([video_url])
                else:
                    print("Видео не найдено.")
            elif mode == 'url':
                ydl.download([url])

        except Exception as e:
            print(f"Ошибка при скачивании: {str(e)}")

    return output_path


# Детекция сцен с помощью PySceneDetect
def detect_scenes(video_path, threshold=30.0):
    video_manager = VideoManager([video_path])
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector(threshold=threshold))
    
    video_manager.start()
    scene_manager.detect_scenes(frame_source=video_manager)
    scene_list = scene_manager.get_scene_list()
    video_manager.release()
    
    # Список сцен в формате (start_time, end_time) в секундах
    scenes = [(scene[0].get_seconds(), scene[1].get_seconds()) for scene in scene_list]
    print(f"Найдено {len(scenes)} сцен.")
    return scenes


def resize_to_vertical_3_4(clip, target_resolution=(960, 1280)):
    w_target, h_target = target_resolution
    clip_resized = clip.resize(height=h_target)

    if clip_resized.w > w_target:
        x_center = clip_resized.w / 2
        clip_resized = clip_resized.crop(
            x_center=x_center, width=w_target, height=h_target
        )
    else:
        pass
    
    return clip_resized


# Выбор и нарезка сцен для итогового клипа длительностью 45 секунд
def create_final_clip(video, scenes, final_duration=45):
    # selected_clips = []
    # accumulated = 0.0

    # for start, end in scenes:
    #     scene_duration = end - start
    #     if accumulated + scene_duration < final_duration:
    #         clip = video.subclip(start, end)
    #         clip = resize_to_vertical_3_4(clip)
    #         selected_clips.append(clip)
    #         accumulated += scene_duration
    #     else:
    #         remaining = final_duration - accumulated
    #         if remaining > 0:
    #             clip = video.subclip(start, start + remaining)
    #             clip = resize_to_vertical_3_4(clip)
    #             selected_clips.append(clip)
    #             accumulated += remaining
    #         break

    # if accumulated < final_duration:
    #     last_clip = video.subclip(video.duration - (final_duration - accumulated), video.duration)
    #     last_clip = resize_to_vertical_3_4(last_clip)
    #     selected_clips.append(last_clip)
    #     accumulated = final_duration

    # final_clip = concatenate_videoclips(selected_clips)

    # final_clip = final_clip.fx(vfx.fadeout, duration=2)
    # if final_clip.audio:
    #     final_clip.audio = final_clip.audio.fx(afx.audio_fadeout, duration=2)

    duration = min(final_duration, video.duration)
    clip = video.subclip(0, duration)
    clip = resize_to_vertical_3_4(clip)

    # Добавим эффект затухания
    clip = clip.fx(vfx.fadeout, duration=2)
    if clip.audio:
        clip.audio = clip.audio.fx(afx.audio_fadeout, duration=2)

    return clip


def process_range(start, end):
    movies = Movies('kp_final')
    
    for i in range(start, end):
        try:
            data_dict = movies.get_data_one_row(i)
            video_path = download_trailer(data_dict, mode='not_url')
            
            video = VideoFileClip(video_path)

            scenes = [(0, min(45, video.duration))]
            final_clip = create_final_clip(video, scenes, final_duration=45)

            output_path = f'./app/static/clips/{data_dict["id"]}.mp4'
            final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", verbose=False, logger=None)

            print(f'[Поток {start}-{end}] Клип {data_dict["id"]} создан, i: {i}')

            video.close()
            final_clip.close()

            os.remove(video_path)

        except Exception as e:
            print(f'[Поток {start}-{end}] Ошибка при обработке i={i}: {e}')


def main():
    movies = Movies('kp_final')

    urls = ['https://www.youtube.com/watch?v=kgAeKpAPOYk']
    
    ids = [326]
    
    for i, url in enumerate(urls):
        data_dict = movies.get_data_one_row(i)
        data_dict['id'] = ids[i]
        video_path = download_trailer(data_dict, url, mode='url')

        video = VideoFileClip(video_path)

        scenes = [(0, min(45, video.duration))]
        final_clip = create_final_clip(video, scenes, final_duration=45)

        output_path = f'./app/static/clips/{data_dict["id"]}.mp4'
        final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", verbose=False, logger=None)

        print(f'Клип {data_dict["id"]} создан, i: {i}')

        video.close()
        final_clip.close()

        os.remove(video_path)


def main_parallel():
    ranges = [(359, 500), (885, 1000), (1391, 1500), (1911, 2000)]
    threads = []

    for start, end in ranges:
        t = threading.Thread(target=process_range, args=(start, end))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("Готово!")


if __name__ == '__main__':
    main()

    # with open("log.txt", "w", encoding="utf-8") as f:
    #     # Перенаправляем stdout и stderr
    #     sys.stdout = f
    #     sys.stderr = f
    #     try:
    #         main_parallel()
    #     finally:
    #         # Важно: вернуть вывод в консоль, если нужно
    #         sys.stdout = sys.__stdout__
    #         sys.stderr = sys.__stderr__
    
