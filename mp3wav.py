import random
import subprocess
from pydub import AudioSegment
from pathlib import Path
import zipfile
import os
import sys

search_files = []
LogBool = True
x = ''

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def mylogika():
    global search_files, x, LogBool
    search_files = [f for f in os.listdir(f'{cwd}\\') if f.endswith('.mp3')]
    if search_files:
        print('Было найдено: ')
        for i, res in enumerate(search_files):
            print(i, ":", res)

        while LogBool:
            z = input('Хотите продолжить? Программа начнет процесс конвертации или склеивания и конвертации, либо '
                      'завершить программу без внесения изменений? [1 или 2]: ')
            if z == '1':
                if len(search_files) == 1:
                    silence = AudioSegment.silent(duration=0)
                else:
                    silence = AudioSegment.silent(duration=3000)  # пауза
                AUDIO_FILES = [AudioSegment.from_mp3(audio_file) + silence for audio_file in search_files]
                random.shuffle(AUDIO_FILES)  # миксер
                sum(AUDIO_FILES).export("{0}.mp3".format(export_path), format="mp3")
                coder_process = subprocess.Popen(['ffmpeg', '-i', export_path + '.mp3', export_path + '.wma'])  # кодер
                coder_process.wait()
                LogBool = False
            elif z == '2':
                sys.exit()
            else:
                print('Попробуйте еще раз, но выберите что-либо из вариантов "1" или "2".')
    else:
        z = input(f'В исходной директории отсутствуют файлы формата .mp3, нажмите "Enter" для выхода из программы')
        sys.exit()
    LogBool = True


cwd = resource_path(Path.cwd())
path1 = f'{cwd}\\Resources\\chaoticimpulse.mp3'
path2 = f'{cwd}\\Resources\\chaoticimpulse.wma'
export_path = f'{cwd}\\Resources\\chaoticimpulse'
if not os.path.exists(f'{cwd}\\Resources\\'):  # проверка на существование каталога Resourses
    os.mkdir(f'{cwd}\\Resources\\')
if os.path.exists(path2):  # удаление актуального .wma и его бэкап по условию
    while LogBool:
        x = input('Хотите сделать бэкап исходного файла "chaoticimpulse.wma"? [y/n]: ')
        if x == 'y':
            if os.path.exists(f'{cwd}\\backup_chaoticimpulse.zip'):
                while LogBool:
                    x = input(f'По пути {cwd}\\backup_chaoticimpulse.zip уже имеется файл с таким именем, продолжить и '
                              f'перезаписать или отменить создание бэкапа? [1 или 2]: ')
                    if x == '1':
                        with zipfile.ZipFile('backup_chaoticimpulse.zip', 'w') as myzip:
                            myzip.write('Resources\\chaoticimpulse.wma')
                        print(f'Исходный файл упакован в "zip" и находится по пути "{cwd}\\backup_chaoticimpulse.zip".')
                        LogBool = False
                    elif x == '2':
                        LogBool = False
                        print('Хорошо! Бэкап небыл перезаписан.')
                    else:
                        print('Попробуйте еще раз, но выберите что-либо из вариантов "1" или "2".')
            else:
                with zipfile.ZipFile('backup_chaoticimpulse.zip', 'w') as myzip:
                    myzip.write('Resources\\chaoticimpulse.wma')
                print(f'Исходный файл упакован в "zip" и находится по пути "{cwd}\\backup_chaoticimpulse.zip".')
                LogBool = False
        elif x == 'n':
            os.remove(path2)
            LogBool = False
        else:
            print('Попробуйте еще раз, но выберите что-либо из вариантов "y" или "n".')
        x = ''
LogBool = True

while LogBool:
    x = input('Программа начинает поиск ".mp3" файлов в исходном каталоге, вы готовы? [y/n]: ')
    if x == 'y':
        mylogika()
        if os.path.exists(path1):  # удаление промежуточного .mp3
            os.remove(path1)
        while LogBool:
            x = input('Хотите удалить исходные файлы сборки? [y/n]: ')
            if x == 'y':
                for filename in search_files:
                    Path(filename).unlink()
                LogBool = False
                z = input('Готово! Нажмите "Enter" для выхода из программы.')
            elif x == 'n':
                LogBool = False
                z = input('Готово! Нажмите "Enter" для выхода из программы.')
            else:
                print('Попробуйте еще раз, но выберите что-либо из вариантов "y" или "n".')
    elif x == 'n':
        LogBool = False
        z = input('Хорошо! Нажмите "Enter" для выхода из программы.')
    else:
        print('Попробуйте еще раз, но выберите что-либо из вариантов "y" или "n".')
