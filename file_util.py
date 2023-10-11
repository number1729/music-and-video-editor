import os

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