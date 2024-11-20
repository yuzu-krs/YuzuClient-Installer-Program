import os
import sys
import requests
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk  # 背景画像表示のためにPillowを使用
import pygame  # 音楽再生のためにpygameを使用

# 実行ファイルがPyInstallerでビルドされたかどうかのチェック
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS  # PyInstallerでビルドされた場合のリソースパス
else:
    base_path = os.path.abspath(".")  # 開発環境の場合のパス

# リソースファイルのパス設定
background_image_path = os.path.join(base_path, "background.png")
background_music_path = os.path.join(base_path, "background.mp3")
icon_path = os.path.join(base_path, "yuzu.ico")

# ダウンロード関数
def download_file(url, save_path, progress_var):
    if os.path.exists(save_path):  # ファイルがすでに存在するか確認
        print(f"{save_path} はすでに存在します。ダウンロードをスキップします。")
        return  # ファイルが存在する場合はダウンロードをスキップ

    response = requests.get(url, stream=True)
    response.raise_for_status()

    total_size = int(response.headers.get('Content-Length', 0))
    with open(save_path, 'wb') as file:  # 'wb'モードでファイルを開くと既存ファイルは上書きされる
        downloaded = 0
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    progress_var.set((downloaded / total_size) * 100)
                root.update_idletasks()

def start_download():
    # ダウンロード開始ボタンを無効化し、テキストを変更
    download_button.config(state="disabled", text="ダウンロード中...")
    progress_bar.place(relx=0.5, rely=0.6, anchor="center")  # プログレスバーを表示

    # ダウンロード対象のURLリスト
    urls = [
        "https://github.com/yuzu-krs/YuzuClientInstaller/raw/refs/heads/main/YuzuClient.jar",
        "https://github.com/yuzu-krs/YuzuClientInstaller/raw/refs/heads/main/steve.mp3",
        "https://github.com/yuzu-krs/YuzuClientInstaller/raw/refs/heads/main/YuzuClient.json"
    ]
    save_dir = os.path.join(os.getenv("APPDATA"), ".minecraft", "versions", "YuzuClient")
    os.makedirs(save_dir, exist_ok=True)

    progress_var.set(0)
    for url in urls:
        filename = url.split("/")[-1]
        save_path = os.path.join(save_dir, filename)
        download_file(url, save_path, progress_var)

    progress_bar.place_forget()  # ダウンロード完了後に進行状況バーを非表示
    download_button.config(state="disabled", text="ダウンロード完了!")  # ダウンロード完了後はボタンを無効にする
    close_button.place(relx=0.5, rely=0.6, anchor="center")  # 閉じるボタンを表示

# 背景音楽再生の設定
def play_background_music():
    pygame.mixer.init()  # pygameのミキサーを初期化
    pygame.mixer.music.load(background_music_path)  # 音楽ファイルの読み込み
    pygame.mixer.music.set_volume(0.1)  # 音量を設定（0.0〜1.0の範囲）
    pygame.mixer.music.play(-1)  # 音楽をループで再生

# GUI作成
root = tk.Tk()
root.title("YuzuClient - Installer")
root.geometry("800x600")  # ウィンドウのサイズを指定
root.resizable(False, False)  # ウィンドウのリサイズを無効化

# アイコン設定
root.iconbitmap(icon_path)  # アイコンを設定

# 背景画像の設定
background_image = Image.open(background_image_path)  # 背景画像を読み込む
background_image = background_image.resize((800, 600), Image.Resampling.LANCZOS)  # ウィンドウサイズに合わせてリサイズ
bg = ImageTk.PhotoImage(background_image)

canvas = tk.Canvas(root, width=800, height=600)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg, anchor="nw")

# 進行状況バー
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, length=400, mode='determinate', variable=progress_var)

# ボタンデザイン
button_style = {
    "bg": "#4CAF50",  # グリーン系
    "fg": "white",
    "font": ("Arial", 12, "bold"),
    "activebackground": "#45a049",
    "relief": "raised",
    "bd": 5,
    "cursor": "hand2"
}

# マインクラフトの起動に関するメッセージラベル
info_label = tk.Label(root, text="ver1.8.8のマインクラフトを１度起動する必要があります。", font=("Arial", 12), fg="red", bg="#f0f0f0")
info_label.place(relx=0.5, rely=0.4, anchor="center")  # ボタンの上に表示

# ダウンロード開始ボタン
download_button = tk.Button(root, text="ダウンロード開始", command=start_download, **button_style)
download_button.place(relx=0.5, rely=0.5, anchor="center")  # ウィンドウ中央に配置

# 閉じるボタン
close_button = tk.Button(root, text="閉じる", command=root.quit, **button_style)
close_button.place_forget()  # 初期状態では非表示

# 背景音楽を再生
play_background_music()

root.mainloop()
