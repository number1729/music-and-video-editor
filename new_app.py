import flet as ft
import pathlib 
import util

class Select_Option(ft.UserControl):
    def __init__(self,file_path: pathlib.Path):
        super().__init__()
        self.option = ft.Column()
        self.file_path = file_path
        self.start_time = 1
        self.end_time = 0


    def build(self):
        return ft.Column([
            ft.Row([
            ft.OutlinedButton("時間で切り抜く", on_click=self.on_time_edit_click),
            ft.OutlinedButton("語句で切り抜く", on_click=self.on_word_edit_click),]),
            self.option])
    
    def on_time_edit_click(self,e):
        music_len = util.get_music_len(self.file_path)
        self.option.controls = [
            ft.Text("開始時間と終了時間を秒数で選択してください。"),
            ft.RangeSlider(
                round=1,
                min=0,
                max=music_len,
                start_value=0,
                divisions=500,
                end_value=music_len,
                inactive_color=ft.colors.GREEN_300,
                active_color=ft.colors.GREEN_700,
                overlay_color=ft.colors.GREEN_100,
                on_change_end=self.on_change_slider,
                label="{value}s",
                ),
            ft.Row([ft.TextField(label="開始時間",value=f"{self.start_time}秒"),ft.TextField(label="終了時間",value=f"{self.end_time}秒")]),
        ]
        self.option.update()
    
    def on_word_edit_click(self,e):
        pass
    
    def on_change_slider(self,e):
        self.start_time = e.control.start_value
        self.end_time = e.control.end_value
        self.option.update()

class Target_File(ft.UserControl):
    def __init__(self, file_path: pathlib.Path):
        super().__init__()
        self.file_path = file_path
        self.file_name = file_path.name
        self.option = Select_Option(file_path)
        
    def build(self):
        return ft.Column([
            ft.Row([ft.Text(self.file_name) , ft.Text(str(self.file_path),color=ft.colors.GREY)]),
            ft.Divider(),
            ft.Text("切り抜く方法を選択してください。"),
            self.option
        ])


class Music_File_Editor(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.selected_files: ft.Column = ft.Column()
        self.pick_files_dialog: ft.FilePicker = ft.FilePicker(on_result=self.pick_files_result)
    
    def did_mount(self):

        self.page.overlay.append(self.pick_files_dialog)
        self.page.update()
        
    def pick_files_result(self,e: ft.FilePickerResultEvent) -> None:
        self.selected_files.controls = list(map(lambda f: Target_File(pathlib.Path(f.path)), e.files))
        self.selected_files.update()
        
    def build(self):


        return ft.Column(
        [
            ft.Text("このアプリは音楽ファイルや動画ファイルの切り抜きを行うアプリです。切り抜きたいファイルを選択してください。"),
            ft.ElevatedButton(
                "Pick files",
                icon=ft.icons.UPLOAD_FILE,
                on_click=lambda _: self.pick_files_dialog.pick_files(
                ),
            ),
            self.selected_files,
        ])



def main(page: ft.Page):
    page.title = "Music File Editor"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update
    music_app = Music_File_Editor()
    page.add(music_app)

ft.app(target=main)
