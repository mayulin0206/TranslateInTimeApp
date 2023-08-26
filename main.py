# 在代码开始的位置导入 PySimpleGUI 库
import PySimpleGUI as sg
from paddleocr import PaddleOCR, draw_ocr
from PIL import ImageGrab
import cv2


global img
global point1, point2

# 就显示一个多行文本框，大小是 50 * 5，单位是应为字符，并通过 disabled 禁止用户编辑内容，使其只读
layout = [  [sg.Multiline( size = (50, 5), key = "-MSG_SCREEN-", do_not_clear=True, disabled=True)]]
window = sg.Window("Msg App", layout = layout)

def on_mouse(event, x, y, flags, param):
    print("on_mouse\n")
    global img, point1, point2
    img2 = img.copy()
    if event == cv2.EVENT_LBUTTONDOWN:  # 左键点击
        point1 = (x, y)
        cv2.circle(img2, point1, 10, (0, 255, 0), thickness=2)
        cv2.imshow('image', img2)
    elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON):  # 按住左键拖曳
        cv2.rectangle(img2, point1, (x, y), (255, 0, 0), thickness=2)
        cv2.imshow('image', img2)
    elif event == cv2.EVENT_LBUTTONUP:  # 左键释放
        point2 = (x, y)
        cv2.rectangle(img2, point1, point2, (0, 0, 255), thickness=2)
        cv2.imshow('image', img2)

def getScreen():

    print('等到3秒，请切换到录屏的页面')
    time.sleep(3)

    curScreen = ImageGrab.grab()  # 获取屏幕对象
    point1, point2 = select_roi(curScreen)
    min_x = min(point1[0], point2[0])
    min_y = min(point1[1], point2[1])
    max_x = max(point1[0], point2[0])
    max_y = max(point1[1], point2[1])
    height, width = max_y - min_y, max_x - min_x

    return min_x,min_y,max_x,max_y

min_x,min_y,max_x,max_y = getScreen()
ocr = PaddleOCR(use_angle_cls=True, lang="en")
# 主线程里的死循环
while True:
    # 使用 read 函数异步模式，100 毫秒超时，通过 timeout_key 自定义了超时 event 的名称
    event, values = window.read(timeout = 100, timeout_key = "-TIMEOUT-")
    
    captureImage = ImageGrab.grab()  # 抓取屏幕
    frame = cv2.cvtColor(np.array(captureImage), cv2.COLOR_RGB2BGR)
    frame = frame[min_y:max_y, min_x:max_x, :]

    result = ocr.ocr(frame, cls=True)
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            print("*********************************************")
            print(translateWord(line[-1][0]))
            print("*********************************************")


    if event is None :
        break

    if event == "-TIMEOUT-":
        try:
            msg = que.get_nowait()
        except Exception:
            # 可能捕获 queue.Empty 异常，no new msg
            continue
        else:
            # que 中有新消息
            # 获取当前显示内容
            old_sreen = values["-MSG_SCREEN-"]

            # 获得消息正文、来源姓名
            new_msg = msg["msg"]
            from_ = msg["from"]

            # 按格式，拼接一行消息
            new_msg_line = "{}: {}".format(from_, new_msg) 

            # 将新消息追加到多行文本结尾
            new_screen = "{}{}".format(old_sreen, new_msg_line) if old_sreen != "" else new_msg_line

            # 将新数据更新到视窗
            window["-MSG_SCREEN-"].update(new_screen)