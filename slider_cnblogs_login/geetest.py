from selenium import webdriver

# 步骤
# 1 图片展开之前的准备工作
# 2 获取图片，生成Image对象
# 3 分析Image对象，计算出缺口的位置，返回需要移动的距离。
# 4 根据上一步移动的距离，移动滑块。
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import time
import random
from PIL import Image, ImageChops, ImageFilter
from io import BytesIO
import numpy as np
import pytweening


def get_trace_list(dis):
    result = []
    pre = 0
    for i in range(1, dis + 1):
        # 获取位移的比例
        y = pytweening.easeOutQuad(i / dis)
        v = round(dis * y)
        result.append(v - pre)
        pre = v
    return result


def pause(min_time=1, max_time=2):
    """
    随机暂停参数指定的时间。单位：秒。

    :param min_time: 最短的暂停时间。
    :param max_time: 最长的暂停时间。
    """
    time.sleep(random.uniform(min_time, max_time))


def prepare():
    """
    图片展开之前的准备工作。
    """
    driver.get("https://passport.cnblogs.com/user/signin")
    driver.maximize_window()
    driver.find_element_by_id("input1").send_keys("a")
    driver.find_element_by_id("input2").send_keys("b")
    driver.find_element_by_id("signin").click()
    # 等待按钮能够点击
    wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "div.geetest_radar_tip")))
    pause()
    driver.find_element_by_css_selector("div.geetest_radar_tip").click()
    # 等待图片可见
    wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "canvas.geetest_canvas_fullbg")))


def cut_image(element):
    """
    根据element所表示的元素，截取该元素的截图，并返回Image对象。
    :param element: 代表图像的元素
    :return: 返回截取之后的Image对象。
    """
    # 获取屏幕截图的二进制bytes（数组）。
    image_bytes = driver.get_screenshot_as_png()
    full_image = Image.open(BytesIO(image_bytes))
    x, y = element.location["x"], element.location["y"]
    # 此处无法获取size
    # width, height = element.size["width"], element.size["height"]
    # 注意：height与width是字符串类型，需要进行转换。
    width, height = int(element.get_attribute("width")), int(element.get_attribute("height"))
    return full_image.crop( (x, y, x + width, y + height))



def get_image():
    """
    获取我们需要分析的图片，并返回。
    :return: 返回需要分析的图片。
    """
    # 很遗憾，元素的截图操作，Chrome浏览器不支持。
    # bg_element = driver.find_element_by_css_selector("geetest_canvas_fullbg")
    # bg_element.screenshot()
    pause()
    bg_element = driver.find_element_by_css_selector("canvas.geetest_canvas_fullbg")
    bg_image = cut_image(bg_element)
    bg_image.save("1.png")
    driver.find_element_by_css_selector("div.geetest_slider_button").click()
    # 等待，确保图片红条消失。
    pause(3, 3.5)
    # 注意：当点击滑块按钮后，背景元素会发生改变。
    bg_element2 = driver.find_element_by_css_selector("canvas.geetest_canvas_slice")
    bg_image2 = cut_image(bg_element2)
    bg_image2.save("2.png")
    # 隐藏滑块图片，并截图。
    driver.execute_script("arguments[0].style.opacity = 0;", bg_element2)
    pause()
    bg_image3 = cut_image(bg_element2)
    bg_image3.save("3.png")
    # 返回最开始的图片，还有缺口与滑块的图片与只含有缺口，而没有滑块的图片。
    return bg_image, bg_image2, bg_image3



def get_edge(image1, image2):
    # 将两个Image图像对象进行差值化，返回差值之后的图像对象（Image）
    differ = ImageChops.difference(image1, image2)
    differ = differ.convert("L")
    differ = differ.filter(ImageFilter.FIND_EDGES)
    differ_array = np.array(differ)
    for i in range(differ.width):
        tmp_array = differ_array[:, i]
        if len(tmp_array[tmp_array > 100]) > 10:
            return i
    print("判定失败")
    return 0




def move(dis):
    action =  ActionChains(driver)
    action.click_and_hold(driver.find_element_by_css_selector("div.geetest_slider_button"))
    trace_list = get_trace_list(dis)
    for i in trace_list:
        action.move_by_offset(i, 0)
    action.release().perform()



def main():
    prepare()
    bg_image, bg_image2, bg_image3 = get_image()
    # 获取滑块的起始位置
    edge1 = get_edge(bg_image, bg_image2)
    # 获取缺口的起始位置
    edge2 = get_edge(bg_image, bg_image3)
    print(edge1, edge2)
    print(edge2 - edge1)
    move(edge2 - edge1)

if __name__ == "__main__":
    driver = webdriver.Chrome(executable_path=r"..\depend_soft\chromedriver")
    wait = WebDriverWait(driver, 10)
    main()


