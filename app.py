import streamlit as st
st.set_page_config(page_title="🎨 多模态可视化平台", layout="wide")

# 再定义函数
def local_css(css_file):
    with open(css_file, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("C:/Users/ziheW/OneDrive/Desktop/python/python数据分析/第十周/Streamlit_UI_Template/templates/template1_style.css")

from 第十周文件上传题 import Point, PointPlotter, ArrayPlotter, AudioPlotter, TextPlotter, ImagePlotter

st.markdown(
    """
    <style>
    .big-font {
        font-size:32px !important;
        font-weight: bold;
        color: #2c3e50;
    }
    .section {
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid #ddd;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<p class="big-font">🎨 多模态数据可视化平台</p>', unsafe_allow_html=True)
st.caption("请选择你要处理的数据类型，并上传或输入数据以生成图表")

option = st.sidebar.selectbox(
    "👉 选择数据类型",
    ("点型数据（Point）", "数组型数据（Array）", "音频数据（Audio）", "文本数据（Text）", "图片数据（Image）")
)

# ---------------------- 点型数据 ----------------------
if option == "点型数据（Point）":
    st.markdown('<div class="section"></div>', unsafe_allow_html=True)
    st.subheader("🟢 点型数据绘图")
    st.caption("请输入多个坐标点，例如：(1,2);(2,3);(3,5)")

    data_str = st.text_input("点坐标：")
    if st.button("🎯 绘图", key="point_plot"):
        try:
            points = [Point(float(x), float(y)) for x, y in [tuple(map(float, p.strip("()").split(","))) for p in data_str.split(";")]]
            plotter = PointPlotter()
            plotter.plot(points)
            st.pyplot()
        except:
            st.error("❌ 输入格式错误！请用 (x,y);(x,y) 格式。")

# ---------------------- 数组型数据 ----------------------
elif option == "数组型数据（Array）":
    st.markdown('<div class="section"></div>', unsafe_allow_html=True)
    st.subheader("🔷 数组数据绘图")
    dim = st.radio("选择维度", ("二维", "三维"))
    st.caption("请输入二维或三维数组数据，每行一组，用英文逗号分隔")
    arr_input = st.text_area("示例：1,2,3\\n4,5,6")

    if st.button("📈 绘图", key="array_plot"):
        try:
            lines = [list(map(float, row.split(","))) for row in arr_input.strip().split("\n")]
            plotter = ArrayPlotter()
            plotter.plot(lines)
            st.pyplot()
        except:
            st.error("❌ 输入格式错误！")

# ---------------------- 音频 ----------------------
elif option == "音频数据（Audio）":
    st.markdown('<div class="section"></div>', unsafe_allow_html=True)
    st.subheader("🔊 音频可视化")
    uploaded_file = st.file_uploader("上传音频文件（支持 .mp3/.wav）", type=["mp3", "wav"])
    mode = st.radio("选择可视化类型", ("waveform", "spectrogram"))

    if uploaded_file and st.button("🎧 播放与绘图", key="audio_plot"):
        with open("temp_audio", "wb") as f:
            f.write(uploaded_file.read())
        plotter = AudioPlotter()
        plotter.plot("temp_audio", plot_type=mode)
        st.pyplot()

# ---------------------- 文本 ----------------------
elif option == "文本数据（Text）":
    st.markdown('<div class="section"></div>', unsafe_allow_html=True)
    st.subheader("📄 文本词云生成")
    text_input = st.text_area("请输入文本内容", "我爱人工智能，人工智能改变世界。")
    if st.button("☁️ 生成词云", key="text_plot"):
        plotter = TextPlotter()
        plotter.plot(text_input, font_path="C:\\Windows\\Fonts\\msyh.ttc")
        st.pyplot()

# ---------------------- 图片 ----------------------
elif option == "图片数据（Image）":
    st.markdown('<div class="section"></div>', unsafe_allow_html=True)
    st.subheader("🖼️ 多图展示（支持拼图 / 心形布局）")
    images = st.file_uploader("上传多张图片", accept_multiple_files=True, type=["png", "jpg", "jpeg"])
    layout = st.radio("选择图片布局样式", ["grid", "heart"], horizontal=True)
    if layout == "grid":
        cols = st.slider("选择每行显示张数", 1, 5, 2)
    else:
        cols = None  # 心形图不需要列数

    if images and st.button("🧩 显示图片", key="img_plot"):
        paths = []
        for i, file in enumerate(images):
            path = f"temp_image_{i}.png"
            with open(path, "wb") as f:
                f.write(file.read())
            paths.append(path)
        plotter = ImagePlotter()
        if layout == "grid":
            plotter.plot(paths, cols=cols, layout="grid")
        else:
            plotter.plot(paths, layout="heart")
        st.pyplot()