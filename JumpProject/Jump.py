
# coding: utf-8
'''
# 注意，当前只针对 1080*1920 分辨率，其他分辨率需作出相应的修改。
#
# === 思路 ===
# 核心思想：每次落稳之后截图，根据截图找出棋子的坐标和下一个块顶面的中点坐标，确定距离
# 识别棋子：由于棋子本身的大小颜色基本保持不变，模板匹配的准确率很高，直接采用OpenCV的相应模块。
# 识别棋盘：由于图像中椭圆和长方形的比例都是确定的，有X轴距离就可以确定需要跳的距离了。
#      So，不管是椭圆还是长方形，找出顶上的尖点即可。简单带来的风险是，但凡哪次没跳到中心，
#      下次就可能不太准确。还好，参数调好的情况下，出错直接导致game over的概率比较小。
'''
import os
import time
import numpy as np
import cv2

chess = cv2.imread('chess.png')
chess_h, chess_w, _ = chess.shape


def get_screenshot():
    os.system('adb shell screencap -p /sdcard/autojump.png')
    os.system('adb pull /sdcard/autojump.png .')


def find_chess(im):
    global chess
    match_score = cv2.matchTemplate(im, chess, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(match_score)
    return max_val, max_loc


def find_next_top(im):
    canny_img = cv2.Canny(im, 1, 10)
    return np.where(canny_img == 255)[1][0]


def jump(distance):
    # 这个参数还需要针对屏幕分辨率进行优化
    press_time = int(distance * 1.575)
    cmd = 'adb shell input swipe 643 1560 643 1560 ' + str(press_time)  # '重新开始'的坐标
    os.system(cmd)


def main():
    while True:
        get_screenshot()
        im = cv2.imread('autojump.png')
        match_score, chess_loc = find_chess(im)
        # 如果匹配分数太低，找不到棋子，应该不是游戏进行中的画面，返回。
        if match_score < 0.7:
            break
        # 根据当前棋子位置确定下一个目标顶点可能的存在区域
        if chess_loc[0] < 540:
            ROI_w = 1080 - (chess_loc[0] + chess_w)
            ROI_h = ROI_w * 5 / 7
            ROI = im[chess_loc[1] + chess_h / 2 - ROI_h: chess_loc[1] + chess_h / 2, \
                  chess_loc[0] + chess_w + 10: chess_loc[0] + chess_w + ROI_w]
        else:
            ROI_w = chess_loc[0]
            ROI_h = ROI_w * 5 / 7
            ROI = im[chess_loc[1] + chess_h / 2 - ROI_h: chess_loc[1] + chess_h / 2, \
                  0:ROI_w - 10]

        # 寻找下一个目标的顶点x轴坐标
        target_x = find_next_top(ROI) + 1
        distance = 0
        if chess_loc[0] < 540:
            distance = target_x + 10 + chess_w
        else:
            distance = ROI_w - target_x + chess_w / 2 + 10

        jump(distance)
        time.sleep(1.3)


if __name__ == '__main__':
    main()