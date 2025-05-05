import jieba
from wordcloud import WordCloud
import librosa
import librosa.display
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np
from PIL import Image

# 抽象类 Plotter
class Plotter(ABC):
    @abstractmethod
    def plot(self, data, *args, **kwargs):
        pass

# 定义一个 Point 类，用于封装 (x, y) 坐标
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# 子类：PointPlotter，实现点型数据的绘制
class PointPlotter(Plotter):
    def plot(self, data, *args, **kwargs):
        x_vals = [point.x for point in data]
        y_vals = [point.y for point in data]

        plt.figure(figsize=kwargs.get("figsize", (6, 4)))
        plt.scatter(x_vals, y_vals, color=kwargs.get("color", "blue"), marker=kwargs.get("marker", "o"))
        plt.title("Point Plot")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.grid(True)
        plt.show()

class ArrayPlotter(Plotter):
    def plot(self, data, *args, **kwargs):
        plt.figure(figsize=kwargs.get("figsize", (6, 4)))

        if len(data) == 2:
            # 二维绘图
            plt.plot(data[0], data[1], label='2D Line')
            plt.xlabel("X")
            plt.ylabel("Y")
            plt.title("2D Array Plot")
            plt.grid(True)
            plt.legend()

        elif len(data) == 3:
            # 三维绘图
            fig = plt.figure(figsize=kwargs.get("figsize", (6, 4)))
            ax = fig.add_subplot(111, projection='3d')
            ax.plot3D(data[0], data[1], data[2])
            ax.set_xlabel("X")
            ax.set_ylabel("Y")
            ax.set_zlabel("Z")
            plt.title("3D Array Plot")

        else:
            raise ValueError("ArrayPlotter 只支持二维或三维数据输入。")

        plt.show()

class AudioPlotter(Plotter):
    def plot(self, data, *args, **kwargs):
        try:
            y, sr = librosa.load(data, sr=None, mono=True)
        except Exception as e:
            print(f"加载音频失败：\n{e}")
            return

        plot_type = kwargs.get("plot_type", "waveform")

        if plot_type == "waveform":
            plt.figure(figsize=kwargs.get("figsize", (10, 4)))
            librosa.display.waveshow(y, sr=sr)
            plt.title("Audio Waveform")
            plt.xlabel("Time (s)")
            plt.ylabel("Amplitude")

        elif plot_type == "spectrogram":
            plt.figure(figsize=kwargs.get("figsize", (10, 4)))
            # 转为频谱图
            S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
            S_dB = librosa.power_to_db(S, ref=np.max)
            librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis='mel')
            plt.title("Mel Spectrogram")
            plt.colorbar(format='%+2.0f dB')

        else:
            print(f"未知的 plot_type: {plot_type}")
            return

        plt.grid(True)
        plt.tight_layout()
        plt.show()

class TextPlotter(Plotter):
    def plot(self, data, *args, **kwargs):
        if not isinstance(data, str):
            print("文本数据必须是字符串类型。")
            return
        # 中文分词
        text = " ".join(jieba.cut(data))
        # 获取中文字体路径（默认使用微软雅黑）
        font_path = kwargs.get("font_path", "msyh.ttc")
        # 生成词云
        wc = WordCloud(font_path=font_path,
                       width=800, height=400,
                       background_color="white").generate(text)
        # 绘图
        plt.figure(figsize=(10, 5))
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        plt.title("Text Word Cloud")
        plt.show()

class ImagePlotter(Plotter):
    def plot(self, data, *args, **kwargs):
        if not isinstance(data, list):
            print("图片数据必须是文件路径的列表。")
            return

        layout = kwargs.get("layout", "grid")
        if layout == "grid":
            self._plot_grid(data, kwargs.get("cols", 2))
        elif layout == "heart":
            self._plot_heart(data)
        else:
            print(f"未知布局方式：{layout}（支持 'grid' 或 'heart'）")

    def _plot_grid(self, paths, cols):
        n = len(paths)
        rows = (n + cols - 1) // cols
        fig, axes = plt.subplots(rows, cols, figsize=(cols * 4, rows * 4))
        axes = axes.flatten() if n > 1 else [axes]

        for i in range(n):
            try:
                img = Image.open(paths[i])
                axes[i].imshow(img)
                axes[i].axis("off")
                axes[i].set_title(f"Image {i+1}")
            except Exception as e:
                print(f"无法加载图像 {paths[i]}：{e}")
                axes[i].axis("off")

        for j in range(n, len(axes)):
            axes[j].axis("off")

        plt.suptitle("🖼️ Image Grid")
        plt.tight_layout()
        plt.show()

    def _plot_heart(self, paths):
        fig, ax = plt.subplots(figsize=(8, 8))
        t = np.linspace(0, 2 * np.pi, len(paths))
        x = 16 * np.sin(t)**3
        y = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)

        ax.set_xlim(-20, 20)
        ax.set_ylim(-20, 20)
        ax.axis("off")

        for xi, yi, path in zip(x, y, paths):
            try:
                img = Image.open(path)
                img = img.resize((60, 60))
                imagebox = OffsetImage(img, zoom=1)
                ab = AnnotationBbox(imagebox, (xi, yi), frameon=False)
                ax.add_artist(ab)
            except Exception as e:
                print(f"无法加载图像 {path}：{e}")

        plt.title("❤️ Heart-shaped Image Layout")
        plt.tight_layout()
        plt.show()