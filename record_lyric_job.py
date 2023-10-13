import os
import pandas as pd
import time
import librosa
import whisper
import schedule
import sys

RED = '\033[31m'
GREEN_BOLD = '\033[1;32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
END = '\033[0m'
def print_with_color(text, color):
    print(color + text + END)



def is_valid_transcribe(whisper_df, music_file_path):
    transcribed_len = whisper_df["end"].to_numpy()[-1]
    original_len = librosa.get_duration(path=music_file_path)
    print(transcribed_len, original_len)
    return transcribed_len/original_len > 0.9

def get_lyrics_file_path(folder_name, file_name):
    desktop_path = os.path.expanduser("~/Desktop")
    new_folder_path = os.path.join(desktop_path, folder_name)
    new_folder_path = os.path.join(new_folder_path, "lyrics")
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
    file_path = os.path.join(new_folder_path, file_name)

    return file_path

def transcribe(path,model_quality,is_forced=False):
    print_with_color(path,BLUE)
    model = whisper.load_model(model_quality)
    path = path
    target_file_path = get_lyrics_file_path(
        "edited_files", f"{os.path.basename(path).split('.')[0]}.csv")
    if os.path.exists(target_file_path) & (not is_forced):
        print_with_color("already exists",YELLOW)
        return
    result = model.transcribe(
        path, verbose=True, language="ja")
    df_1 = pd.DataFrame(result["segments"])
    is_valid_transcribe(df_1, path)
    df_1.to_csv(target_file_path)
    
def record_job(dir_path,model_quality):
    print_with_color("record_job_start",GREEN_BOLD)
    print_with_color(model_quality,BLUE)
    files_path_list = os.listdir(dir_path)
    files_path_list = [os.path.join(dir_path, file_path) for file_path in files_path_list if file_path.endswith(
        ".mp3") or file_path.endswith(".mp4")]
    files_path_list
    for file_path in files_path_list:
        transcribe(file_path,model_quality)
    print_with_color("record_job done",GREEN_BOLD)

args = sys.argv
args = args[1:]
if len(args) == 0:
    print_with_color("no args",RED)
    exit()
dir_path = args.pop(0)
if args:
    model_quality = args.pop(0)
else:
    model_quality = "base"

schedule.every().day.at("18:05").do(record_job,dir_path,model_quality)

print_with_color("タスクスケジューラーを起動します",GREEN_BOLD)
while True:
    schedule.run_pending()
    time.sleep(1)