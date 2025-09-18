from PIL import Image,ImageDraw,ImageFont

from PIL import Image, ImageDraw, ImageFont
import random

def check_code(width=120, height=30, char_length=5):
    code = []
    img = Image.new(mode='RGB', size=(width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img, mode='RGB')#创建一个可以在图像上绘制的绘图对象。draw是一个ImageDraw对象
    
    def rndChar():
        """生成随机字母"""
        return chr(random.randint(65, 90))#randint()用于生成一个指定范围内的随机整数
    
    def rndColor():
        """生成随机颜色"""
        return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))
    
    # 写文字
    font = ImageFont.load_default()#字体风格默认
    for i in range(char_length):
        char = rndChar()
        code.append(char)
        h = random.randint(0, 4)
        draw.text([i * width / char_length, h], char,font=font,  fill=rndColor())
    #写点
    for i in range(40):
        draw.point([random.randint(0,width),random.randint(0,height)],fill=rndColor())
    
    
    return img, ''.join(code)  # 返回图片对象和验证码字符串
if __name__ =="__main__":
    img,code=check_code()##？？为什么要这样
    img.save('code.png')
    print(code)

# 使用示例
# img, code = check_code()
# img.save('code.png')  # 保存验证码图片
# print(code)  # 打印验证码内容
