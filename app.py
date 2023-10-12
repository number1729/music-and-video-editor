import flet as ft
import os 
from util import get_files_with_extension, create_folder_and_file_on_desktop, get_start_and_end_time
from pydub import AudioSegment
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import whisper

def main(page):
    
    page.title = "Music File Editor"
    
    def edit(is_mp3,path,start_time,end_time,is_word_edit):
        start_time_value = int(start_time.value)
        end_time_value = int(end_time.value)
        page.clean()
        print(start_time_value,end_time_value)
        if is_mp3:
            audio = AudioSegment.from_mp3(path)
            new_audio = audio[start_time_value*1000:end_time_value*1000]
            path_name = os.path.basename(path)
            file_name = f"{start_time_value}_{end_time_value}_{path_name}"
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
            mp3_files_buttons_view.controls.append(ft.OutlinedButton(text=mp3_files[i], on_click=file_btn_click))

        mp4_files_buttons_view = ft.ListView(expand=1, spacing=10, padding=20)
        mp4_files = get_files_with_extension(directory_path, ".mp4")
        for j in range(len(mp4_files)):
            mp4_files_buttons_view.controls.append(ft.OutlinedButton(text=mp4_files[j], on_click=file_btn_click))

        page.add(ft.Row([mp3_files_buttons_view, mp4_files_buttons_view]))
        
    def do_whisper(e):
        print(1234)
        model = whisper.load_model(model_quality_dropdown.value)
        pb = ft.ProgressBar(width=400, color="amber", bgcolor="#eeeeee")
        page.add(ft.Text("transcribing..."),pb)
        result = model.transcribe(path_ft.value)
        pb.disabled = True
        page.add(ft.Text("transcribed"))
        taget_segment_dict = get_start_and_end_time(result,search_word.value)
        list_view = ft.ListView(expand=1, spacing=10, padding=20)
        page.add(ft.Text(taget_segment_dict))
        
        
        
        


    def word_edit_mode(is_mp3,path):
        path_ft = ft.Text(path)
        print(1)
        model_quality_dropdown = ft.Dropdown(label="model quality", options=[ft.dropdown.Option("base"),
                                                                             ft.dropdown.Option("small"),
                                                                             ft.dropdown.Option("medium"),
                                                                             ft.dropdown.Option("large")])
        print(model_quality_dropdown)
        search_word = ft.TextField(label="search word")
        ok_button   = ft.OutlinedButton("ok", on_click= do_whisper)
        page.add(path_ft,model_quality_dropdown,search_word,ok_button)
        

    
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
        path = os.path.abspath(e.control.text)
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
                mp3_files_buttons_view.controls.append(ft.OutlinedButton(text=mp3_files[i], on_click=file_btn_click))

            mp4_files_buttons_view = ft.ListView(expand=1, spacing=10, padding=20)
            mp4_files = get_files_with_extension(directory_path, ".mp4")
            for j in range(len(mp4_files)):
                mp4_files_buttons_view.controls.append(ft.OutlinedButton(text=mp4_files[j], on_click=file_btn_click))

            page.add(ft.Row([mp3_files_buttons_view, mp4_files_buttons_view]))


    txt_name = ft.TextField(label="フォルダ名を入力してください")

    page.add(txt_name, ft.ElevatedButton("OK", on_click=directory_button_click))

ft.app(target=main)