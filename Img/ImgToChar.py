from PIL import Image

# 灰度值 gray ＝ 0.2126 * r + 0.7152 * g + 0.0722 * b

img_charlist = list(''''@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`' ''')

Width = 300
Height = 225

def get_char(r, g, b, alpha=256):
    if alpha == 0:
        return ' '
    length = len(img_charlist)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)  # 灰度值计算
    unit = (256.0 + 1) / length
    return img_charlist[int(gray/unit)]

if __name__ == '__main__':
    imgPath = 'C:/Users/v_meixfu/Pictures/1529926504593522.jpg'
    img = Image.open(imgPath)
    img = img.resize((Width, Height), Image.NEAREST)
    txt = ""
    for i in range(Height):
        for j in range(Width):
            txt += get_char(*img.getpixel((j, i)))
        txt += '\n'
    print(txt)

    with open('C:/Users/v_meixfu/Desktop/img.txt', 'w') as f:
        f.write(txt)