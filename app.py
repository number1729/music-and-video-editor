import flet as ft
import os 
import pandas as pd
from util import get_files_with_extension, create_folder_and_file_on_desktop,  get_lyric_data, get_lyrics_file_path
from pydub import AudioSegment
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

def main(page):
    
    page.title = "Music File Editor"
    
    def edit(is_mp3,path,start_time,end_time,is_word_edit,word=""):
        if not is_word_edit:
            start_time_value = int(start_time.value)
            end_time_value = int(end_time.value)
        else:
            start_time_value = start_time
            end_time_value = end_time
        page.clean()
        print(start_time_value,end_time_value)
        if is_mp3:
            audio = AudioSegment.from_mp3(path)
            new_audio = audio[start_time_value*1000:end_time_value*1000]
            path_name = os.path.basename(path)
            file_name = f"{start_time_value}_{end_time_value}_{path_name}" if not is_word_edit else f"{word}_{start_time_value}_{end_time_value}_{path_name}"
            output_path = create_folder_and_file_on_desktop("edited_files", file_name)
            new_audio.export(output_path, format="mp3")
        else:
            # mp4の場合
            path_name = os.path.basename(path)
            file_name = f"{start_time_value}_{end_time_value}_{path_name}"

            output_path = create_folder_and_file_on_desktop("edited_files", file_name)
            print(path, start_time_value, end_time_value, output_path)
            ffmpeg_extract_subclip(path, start_time_value, end_time_value, targetname=output_path)
        page.add(ft.Text("edited"))
        directory_path = os.path.dirname(path)
        page.clean()
        page.add(ft.Text(f"your directory, {directory_path}"))
        page.add(ft.Text("Your files:"))
        mp3_files_buttons_view = ft.ListView(expand=1, spacing=10, padding=20)
        mp3_files = get_files_with_extension(directory_path, ".mp3")
        for i in range(len(mp3_files)):
            mp3_files_buttons_view.controls.append(ft.OutlinedButton(text=os.path.basename(mp3_files[i]),data=mp3_files[i], on_click=file_btn_click))

        mp4_files_buttons_view = ft.ListView(expand=1, spacing=10, padding=20)
        mp4_files = get_files_with_extension(directory_path, ".mp4")
        for j in range(len(mp4_files)):
            mp4_files_buttons_view.controls.append(ft.OutlinedButton(text=os.path.basename(mp4_files[j]),data=mp4_files[j], on_click=file_btn_click))

        page.add(ft.Row([mp3_files_buttons_view, mp4_files_buttons_view]))
        
    def edit_from_word(path, word,is_mp3):
        page.clean()
        path_csv = get_lyrics_file_path("edited_files", f"{os.path.basename(path).split('.')[0]}.csv")
        df = pd.read_csv(path_csv)
        lyric_dict_list = get_lyric_data(df,word)
        lv = ft.ListView(expand=1, spacing=10, padding=20)
        for dict_item in lyric_dict_list:
            dict_item["start"] = int(dict_item["start"])
            dict_item["end"] = int(dict_item["end"])
            lv.controls.append(ft.OutlinedButton(text=f"{dict_item['text']}", on_click=lambda e:edit(is_mp3,path,dict_item["start"],dict_item["end"],True,dict_item["text"])))    
        page.add(lv)
        


    def word_edit_mode(is_mp3,path):
        path_ft = ft.Text(path)
        search_word = ft.TextField(label="search word")
        ok_button   = ft.OutlinedButton("ok", on_click= lambda e: edit_from_word(path, search_word.value,is_mp3))
        page.add(path_ft,search_word,ok_button)
        

    
    def time_edit_mode(is_mp3,path):
        page.add(ft.Text("time_edit_mode"))
        start_time = ft.TextField(label="start time")
        end_time = ft.TextField(label="end time")
        page.add(ft.Row([start_time, end_time]))
        page.add(ft.ElevatedButton("edit", on_click=lambda e:edit(is_mp3,path,start_time,end_time,False)))
        if not (start_time.value and end_time.value):
            page.update()
        else:
            start_time_value = int(start_time.value)
            end_time_value = int(end_time.value)
        



 
        
        
    def file_btn_click(e):
        path = os.path.abspath(e.control.data)
        page.clean()
        print(path)
        is_mp3 = path.endswith(".mp3")
        page.add(ft.Text(f"your file, {path}"))
        page.add(ft.Row([ft.ElevatedButton("字句で検索・編集",on_click=lambda e:word_edit_mode(is_mp3,path) ),
                         ft.ElevatedButton("時間で検索・編集",on_click=lambda e:time_edit_mode(is_mp3,path))]))
 
        
    
    def directory_button_click(e):
        if not txt_name.value:
            txt_name.error_text = "フォルダ名を入力してください"
            page.update()
        else:
            directory_path = txt_name.value
            # page.clean()
            page.add(ft.Text(f"フォルダ, {directory_path}"))
            page.add(ft.Text("ファイル:"))
            mp3_files_buttons_view = ft.ListView(expand=1, spacing=10, padding=20)
            mp3_files = get_files_with_extension(directory_path, ".mp3")
            for i in range(len(mp3_files)):
                mp3_files_buttons_view.controls.append(ft.OutlinedButton(text=os.path.basename(mp3_files[i]),data=mp3_files[i], on_click=file_btn_click))

            mp4_files_buttons_view = ft.ListView(expand=1, spacing=10, padding=20)
            mp4_files = get_files_with_extension(directory_path, ".mp4")
            for j in range(len(mp4_files)):
                mp4_files_buttons_view.controls.append(ft.OutlinedButton(text=os.path.basename(mp4_files[j]),data=mp4_files[j], on_click=file_btn_click))

            page.add(ft.Row([mp3_files_buttons_view, mp4_files_buttons_view]))


    txt_name = ft.TextField(label="フォルダ名を入力してください")

    page.add(txt_name, ft.ElevatedButton("OK", on_click=directory_button_click))

ft.app(target=main)