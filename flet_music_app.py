import flet as ft
import pathlib 
import util

LYRICS_FOLDER = "lyrics"

class Select_Option(ft.Column):
    def __init__(self,file_path: pathlib.Path):
        super().__init__()
        self.option = ft.Column()
        self.file_path = file_path
        self.start_time = 0
        self.end_time = 0
        self.time_edit = ft.Row()
        self.done_text = ft.Text("")
        self.lyric_path = file_path.parent / LYRICS_FOLDER / (file_path.stem + ".txt")
        print(type(self.lyric_path),self.lyric_path)


    def build(self):
        return ft.Column([
            ft.Row([
            ft.OutlinedButton("時間で切り抜く", on_click=self.on_time_edit_click),
            # ft.OutlinedButton("語句で切り抜く", on_click=self.on_word_edit_click),
            ]),
            self.option])
    
    def on_time_edit_click(self,e):
        self.option.controls = [
            ft.Text("音楽ファイルを読み込み中..."),
            ft.ProgressBar(),
        ]
        self.option.update()
        self.time_edit_block(e)
        print("time edit")
        self.option.update()
        
    
    def time_edit_block(self,e):
        music_len = util.get_music_len(self.file_path)
        self.time_edit.controls = [
            ft.TextField(label="開始時間",value=f"{float(self.start_time):.1f}"),
            ft.TextField(label="終了時間",value=f"{float(self.end_time):.1f}"),
            ft.Divider(),
            ]
        self.option.controls = [
            ft.Row([ft.Text("開始時間と終了時間を秒数で選択してください。"),ft.Text(f"再生時間({music_len:.1f}s)",color=ft.colors.GREY)]),
            ft.RangeSlider(
                round=1,
                min=0,
                max=music_len,
                start_value=self.start_time,
                divisions=500,
                end_value=self.end_time if self.end_time else music_len,
                inactive_color=ft.colors.GREEN_300,
                active_color=ft.colors.GREEN_700,
                overlay_color=ft.colors.GREEN_100,
                on_change_end=self.on_change_slider,
                label="{value}s",
                ),
            self.time_edit,
            ft.ElevatedButton(text="切り抜く",on_click=self.clicked_edit),
            self.done_text,
        ]
        self.option.update()
    
    def on_word_edit_click(self,e):
        print("word edit",self.lyric_path, self.lyric_path.exists())
        if not self.lyric_path.parent.exists():
            self.lyric_path.parent.mkdir()
        if not self.lyric_path.exists():
            self.option.controls = [ft.Text("歌詞ファイルが見つかりませんでした。歌詞ファイルを作成するには、作成ボタンを押してください。"),
                                    ft.ElevatedButton("作成",on_click=self.create_lyric_file)]
        else:
            self.option.controls = [ft.Text("歌詞ファイルが見つかりました。語句で検索できます。"),
                                    ft.TextField(label="検索語句",on_change=self.on_change_search_word)]
        self.option.update()
        
    def on_change_search_word(self,e):
        search_word = e.control.value
        result = util.search_word(self.lyric_path,search_word)
        print(result)
        self.option.controls = [ft.Text(result)]
        self.option.update()
            
    def create_lyric_file(self,e):
        result = util.voice_to_text(self.file_path)
        util.create_lyric_file(self.lyric_path,result)
        self.on_word_edit_click(e)
        
    def on_change_slider(self,e):
        self.start_time = e.control.start_value
        self.end_time = e.control.end_value
        print(self.start_time,self.end_time,e.control.start_value,e.control.end_value)
        self.time_edit.update()
        self.time_edit_block(e)
    
    def clicked_edit(self,e):
        util.edit(self.file_path,float(self.start_time),float(self.end_time))
        self.done_text = ft.Text("切り抜きが完了しました。")
        self.time_edit_block(e)

class Target_File(ft.Column):
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

class Music_File_Editor(ft.Column):
    def __init__(self):
        super().__init__()
        self.selected_files: ft.Column = ft.Column()
        self.pick_files_dialog: ft.FilePicker = ft.FilePicker(on_result=self.pick_files_result)
    
    def did_mount(self):
        self.page.overlay.append(self.pick_files_dialog)
        self.page.update()
        
    def pick_files_result(self,e: ft.FilePickerResultEvent) -> None:
        if e.files is None:
            return
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
    print("main")
    page.title = "Music File Editor"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update
    music_app = Music_File_Editor()
    page.add(music_app)

ft.app(target=main)
