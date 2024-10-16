import tkinter as tk
from tkinter import filedialog

import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageTk


class Processing:
    def __init__(self, root):
        self.root = root
        root.title("Image Processing")

        # ファイルを開くボタン
        open_button = tk.Button(root, text="ファイルを開く", command=self.Open_File)
        open_button.pack(side=tk.TOP, pady=10)

        # 画像表示用のフレームを作成
        image_frame = tk.Frame(root)
        image_frame.pack(pady=20, side=tk.TOP)

        # 画像表示スペース確保
        self.input_img = tk.Label(image_frame)
        self.input_img.pack(side=tk.LEFT)

        self.output_img = tk.Label(image_frame)
        self.output_img.pack(side=tk.LEFT)

        # 選択されたオプションを格納するための変数　デフォルト：オリジナル
        selected_option = tk.StringVar(value="1")

        # 画像処理のコマンド用ラジオボタン
        self.original = tk.Radiobutton(text="オリジナル", command=self.Original, variable=selected_option, value="1")
        self.original.pack(side=tk.LEFT)

        self.gray_scale = tk.Radiobutton(text="グレースケール", command=self.Gray_Scale, variable=selected_option,
                                         value="2")
        self.gray_scale.pack(side=tk.LEFT)

        self.binarization = tk.Radiobutton(text="2値化", command=self.Binarization, variable=selected_option, value="3")
        self.binarization.pack(side=tk.LEFT)

        self.smoothing = tk.Radiobutton(text="平滑化", command=self.Smoothing, variable=selected_option, value="4")
        self.smoothing.pack(side=tk.LEFT)

        self.contour = tk.Radiobutton(text="輪郭抽出", command=self.Contour, variable=selected_option, value="5")
        self.contour.pack(side=tk.LEFT)

        self.histogram = tk.Radiobutton(text="ヒストグラム表示", command=self.Histogram, variable=selected_option,
                                        value="6")
        self.histogram.pack(side=tk.LEFT)

        self.filename = None  # ファイル名を格納する変数

    def Open_File(self):
        # ファイルダイアログを開き、画像ファイルを選択
        fTyp = [("", "*")]
        self.filename = filedialog.askopenfilename(filetypes=fTyp, initialdir="./")
        # 画像ファイルを読み込み、表示
        if self.filename:
            self.img = Image.open(self.filename)

            # リサイズ処理 ここで横幅を500pxに固定し、縦幅はアスペクト比を維持
            basewidth = 500
            wpercent = (basewidth / float(self.img.size[0]))
            hsize = int((float(self.img.size[1]) * float(wpercent)))
            self.resized_img = self.img.resize((basewidth, hsize), Image.LANCZOS)  # リサイズした画像を self.resized_img に保存

            self.photo = ImageTk.PhotoImage(self.resized_img)  # self.resized_img を使用
            self.input_img.config(image=self.photo)
            self.input_img.image = self.photo

            # 画像処理を実行 (デフォルトはオリジナル)
            self.Original(self.resized_img)  # self.resized_img を Original 関数に渡す

    def Original(self, img):  # img を引数として受け取る
        # オリジナル画像を表示
        self.photo2 = ImageTk.PhotoImage(img)  # img を使用
        self.output_img.config(image=self.photo2)
        self.output_img.image = self.photo2

    def Gray_Scale(self):
        # OpenCVを使ってグレースケール変換
        img_cv = cv2.cvtColor(np.array(self.resized_img), cv2.COLOR_RGB2GRAY)  # self.resized_img を使用
        # PIL画像に変換
        img_pil = Image.fromarray(img_cv)
        # Tkinterで表示できるようPhotoImageに変換
        self.photo2 = ImageTk.PhotoImage(img_pil)
        self.output_img.config(image=self.photo2)
        self.output_img.image = self.photo2

    def Binarization(self):
        # OpenCVを使って2値化
        img_cv = cv2.cvtColor(np.array(self.resized_img), cv2.COLOR_RGB2GRAY)  # self.resized_img を使用
        _, img_binary = cv2.threshold(img_cv, 128, 255, cv2.THRESH_BINARY)
        # PIL画像に変換
        img_pil = Image.fromarray(img_binary)
        # Tkinterで表示できるようPhotoImageに変換
        self.photo2 = ImageTk.PhotoImage(img_pil)
        self.output_img.config(image=self.photo2)
        self.output_img.image = self.photo2

    def Smoothing(self):
        # OpenCVを使って平滑化
        img_cv = cv2.cvtColor(np.array(self.resized_img), cv2.COLOR_RGB2BGR)  # self.resized_img を使用
        img_smooth = cv2.blur(img_cv, (5, 5))
        # PIL画像に変換
        img_pil = Image.fromarray(cv2.cvtColor(img_smooth, cv2.COLOR_BGR2RGB))
        # Tkinterで表示できるようPhotoImageに変換
        self.photo2 = ImageTk.PhotoImage(img_pil)
        self.output_img.config(image=self.photo2)
        self.output_img.image = self.photo2

    def Contour(self):
        # OpenCVを使って輪郭抽出
        img_cv = cv2.cvtColor(np.array(self.resized_img), cv2.COLOR_RGB2GRAY)  # self.resized_img を使用
        edges = cv2.Canny(img_cv, 100, 200)
        # PIL画像に変換
        img_pil = Image.fromarray(edges)
        # Tkinterで表示できるようPhotoImageに変換
        self.photo2 = ImageTk.PhotoImage(img_pil)
        self.output_img.config(image=self.photo2)
        self.output_img.image = self.photo2

    def Histogram(self):
        # OpenCVを使ってヒストグラム表示
        img_cv = cv2.cvtColor(np.array(self.resized_img), cv2.COLOR_RGB2BGR)  # self.resized_img を使用
        color = ('b', 'g', 'r')
        for i, col in enumerate(color):
            hist = cv2.calcHist([img_cv], [i], None, [256], [0, 256])
            plt.plot(hist, color=col)
            plt.xlim([0, 256])
        plt.show()


if __name__ == '__main__':
    root = tk.Tk()
    app = Processing(root)
    root.mainloop()
