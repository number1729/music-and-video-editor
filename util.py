import os
from pydub import AudioSegment
import pathlib
import whisper
import pandas as pd

def get_music_len(path :pathlib.Path):
    audio = AudioSegment.from_file(path)
    return audio.duration_seconds

def edit(path :pathlib.Path, start_time, end_time):
    audio = AudioSegment.from_file(path)
    audio = audio[start_time*1000:end_time*1000]
    start_time = round(start_time,1)
    end_time = round(end_time,1)
    file_name = f"{start_time}_{end_time}_{path.name}"
    file_path = path.parent / "music_edit_files" /file_name
    if not os.path.exists(path.parent / "music_edit_files"):
        os.makedirs(path.parent / "music_edit_files")
    audio.export(file_path, format="mp3")


def voice_to_text(path :pathlib.Path):
    model = whisper.load_model("small")
    result = model.transcribe(str(path), verbose=True, language="ja")
    print(result)
    return result

def create_lyric_file(lyric_path :pathlib.Path, result):
    df = pd.DataFrame(result["segments"])
    df.to_csv(lyric_path)
    print(f"lyric file created at {lyric_path}")

def get_files_with_extension(directory, extension):
    # ディレクトリ内のファイルを取得
    files = os.listdir(directory)

    # 指定した拡張子と一致するファイルを抽出
    matching_files = [file for file in files if file.endswith(extension)]

    # 絶対パスに変換して返す
    matching_files = [os.path.abspath(os.path.join(directory, file)) for file in matching_files]

    return matching_files

def create_folder_and_file_on_desktop(folder_name, file_name):
    # デスクトップのパスを取得
    desktop_path = os.path.expanduser("~/Desktop")

    # 新しいフォルダのパスを生成
    new_folder_path = os.path.join(desktop_path, folder_name)

    # フォルダが存在しない場合、作成
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)

    # ファイルのパスを生成
    file_path = os.path.join(new_folder_path, file_name)

    return file_path

"""
デスクトップにあるフォルダの中にlyricsフォルダを作成し,中にはいるファイルのパスを返す
"""
def get_lyrics_file_path(folder_name, file_name):
         
    desktop_path = os.path.expanduser("~/Desktop")
    new_folder_path = os.path.join(desktop_path, folder_name)
    new_folder_path = os.path.join(new_folder_path, "lyrics")
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
    file_path = os.path.join(new_folder_path, file_name)
    return file_path



def get_lyric_data(df,word):
    return df[df["text"].str.contains(word)][["start", "end", "text"]].to_dict(orient="records")