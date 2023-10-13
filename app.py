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
            new_audio = audio[(start_time_value+1)*1000:(end_time_value+2)*1000]
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
            ffmpeg_extract_subclip(path, start_time_value+1, end_time_value+2, targetname=output_path)
        page.add(ft.Text("edited"))
        extension = ".mp3" if is_mp3 else ".mp4"
        file_button_list(extension)
        
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
    
    def file_button_list(extension):
            next_extension = ".mp4" if extension == ".mp3" else ".mp3"
            change_extension_button = ft.ElevatedButton(f"{next_extension}に変更", on_click= lambda e: file_button_list(next_extension))
            directory_path = txt_name.value
            page.clean()
            page.add(ft.Text(f"フォルダ, {directory_path}"))
            page.add(ft.Text(f"{extension}ファイル:"))
            files_buttons_view = ft.ListView(expand=1, spacing=10, padding=20)
            files = get_files_with_extension(directory_path, extension)
            for i in range(len(files)):
                files_buttons_view.controls.append(ft.OutlinedButton(text=os.path.basename(files[i]),data=files[i], on_click=file_btn_click))
            
            page.add(change_extension_button,files_buttons_view)

    
    def directory_button_click(e):
        if not txt_name.value:
            txt_name.error_text = "フォルダ名を入力してください"
            page.update()
        else:
            extension = ".mp3" if c1.value else ".mp4"
            file_button_list(extension)
            

    txt_name = ft.TextField(label="フォルダ名を入力してください")
    c1 = ft.Switch(label="mp3", value=True)
    page.add(txt_name,c1,ft.ElevatedButton("OK", on_click=directory_button_click))

ft.app(target=main)