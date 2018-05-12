from selenium import webdriver
import requests
from io import BytesIO
from PIL import Image, ImageEnhance
import numpy as np

# 1 准备工作
# 2 获取（下载）图片
# 3 分析图片，得到缺口的位置
# 4 根据缺口位置，进行移动操作
from selenium.webdriver import ActionChains


def prepare():
    """
    执行一些获取图片之前的准备工作。
    """
    driver.get("http://dun.163.com/trial/jigsaw")
    # 最大化窗口
    driver.maximize_window()
    e = driver.find_element_by_css_selector(".is-right .u-mdtitle")
    # 执行JavaScripts语句。arguments可以用来获取实际参数。
    driver.execute_script("arguments[0].scrollIntoView();", e)


def download(selector):
    """根据css选择器下载指定的图片

    :param selector css选择器
    :return 下载之后的image图片对象。
    """
    e = driver.find_element_by_css_selector(selector)
    response = requests.get(e.get_attribute("src"))
    image = Image.open(BytesIO(response.content))
    return image



def get_image():
    """
    处理下载的图像。
    :return: 返回处理后的图像（背景图片与滑块图像）。
    """
    bg_image = download(".is-right img.yidun_bg-img")
    slider_image = download(".is-right img.yidun_jigsaw")
    # 获取图像的最小边界。【将纯黑色区域剪切掉】，返回最小边界的位置。
    # 返回值是一个元组类型。元组中含有4个元素。分别是【左，上，右，下】的坐标位置。
    bound = slider_image.getbbox()
    # 根据指定的边界（bound）进行图片的裁剪。返回裁剪之后的结果。
    slider_image = slider_image.crop(bound)
    slider_image = slider_image.convert("L")
    slider_image = slider_image.point(lambda x: 0 if x == 0 else 255)
    slider_image.save("slider.jpg")
    # 处理图像对比度的操作。
    ie = ImageEnhance.Contrast(bg_image)
    # 调整对比度。参数值越大，越明显。
    bg_image = ie.enhance(100)
    bg_image = bg_image.convert("L")
    # 将背景图像进行裁剪。
    bg_image = bg_image.crop((0, bound[1], bg_image.size[0], bound[3]))
    bg_image.save("bg.jpg")
    return bg_image, slider_image


def get_edge(bg_image, slider_image):
    """
    根据背景图像与滑块图像，寻找缺位的位置。
    :param bg_image: 背景图像
    :param slider_image: 滑块图像
    :return: 背景图像中缺口的位置
    """

    # 接收一个Image对象，返回该Image图像对应的像素值（数组）。
    bg_array = np.array(bg_image)
    slider_array = np.array(slider_image)
    max_match = 0
    match_index = 0
    for i in range(slider_image.size[0], bg_image.size[0] - slider_image.size[0]):
        num = np.sum((bg_array[:, i: i +  slider_image.size[0]] == slider_array) & (slider_array == 255))
        #print(num)
        if num > max_match:
            max_match = num
            match_index = i
    print(match_index)
    return match_index


def move(distance):
    """
    根据参数，将滑块移动指定的距离。
    :param distance: 移动的距离
    """
    slider = driver.find_element_by_css_selector(".is-right div.yidun_slider")
    ActionChains(driver).click_and_hold(slider).perform()
    for i in range(distance):
        ActionChains(driver).move_by_offset(1, 0).perform()
    ActionChains(driver).release().perform()


def main():
    prepare()
    bg_image, slider_image = get_image()
    distance = get_edge(bg_image, slider_image)
    move(distance)



if __name__ == "__main__":
    driver = webdriver.Chrome(executable_path=r"..\depend_soft\chromedriver")
    main()
