import flet as ft
import whisper


def main(page):


    print(1234)
    model = whisper.load_model("base")
    pb = ft.Column([ft.Text("transcribing..."),ft.ProgressBar(width=400, color="amber", bgcolor="#eeeeee")])
    page.add(pb)
    result = model.transcribe("/Users/itouhikaru/Desktop/edited_files/10_44_movie_ver.mp3",verbose=True,language="ja")
    pb.visible = False
    page.update()
    page.add(ft.Text(result["text"]))

    
ft.app(target=main)
