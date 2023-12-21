# 导入所需模块
import cv2
import numpy as np
import os
import pandas as pd
from skimage.feature import peak_local_max
from skimage.segmentation import watershed
from scipy import ndimage

# 定义函数：提取轮廓并计算比例
def extract_contour_and_calculate_ratio(image):

    # 将图像从RGB转为灰度
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 对图像进行二值化处理
    _, thresholded_image = cv2.threshold(grayscale_image, 140, 255, cv2.THRESH_BINARY)
    # 寻找轮廓
    contours, _ = cv2.findContours(thresholded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 创建一个空白图像，与原始图像大小相同
    blank_image = np.zeros(image.shape, dtype=np.uint8)
    # 在空白图像上绘制轮廓
    for contour in contours:
        cv2.drawContours(blank_image, [contour], -1, (255, 255, 255), thickness=-1)
    # 计算对象像素和总像素
    object_pixels = np.sum(blank_image == 255)
    total_pixels = image.shape[0] * image.shape[1]
    # 计算并返回比例
    ratio = round((object_pixels / total_pixels) * 100, 3)
    return ratio, blank_image

# 定义函数：使用分水岭算法提取轮廓并计算比例
def extract_contour_and_calculate_ratio_watershed(image):
    # 在这个函数中，可以调整以下几个参数以改变输出效果:
    #1.`cv2.threshold`函数中的阈值和最大值：这两个参数决定了二值化图像的阈值和最大值。调整这两个参数可以改变二值化图像的效果，从而影响分水岭算法的结果。
    #2.`ndimage.distance_transform_edt`函数：这个函数用于计算二值图像的欧氏距离变换。可以使用其他类型的距离变换，例如曼哈顿距离或切比雪夫距离，看看这是否会改善结果。
    #3.`peak_local_max`函数中的`min_distance`参数：这个参数决定了局部最大值之间的最小距离。增大这个值将会减少局部最大值的数量，这可能会导致分割出更少的区域。反之，减小这个值将会增加局部最大值的数量，可能会导致分割出更多的区域。
    #4.`cv2.drawContours`函数中的线条厚度：这个参数决定了绘制轮廓的线条厚度。增大这个值将会使轮廓线条更粗，可能会使对象的像素数量增加。反之，减小这个值将会使轮廓线条更细，可能会使对象的像素数量减少。

    # 将图像从RGB转为灰度
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 使用Otsu算法对图像进行二值化处理
    _, binary_image = cv2.threshold(grayscale_image, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    # 使用欧氏距离变换计算二值图像的距离图
    distance_transform = ndimage.distance_transform_edt(binary_image)
    # 使用peak_local_max函数找到距离图中的局部最大值（org20）
    coordinates = peak_local_max(distance_transform, labels=binary_image, min_distance=20)
    # 创建一个与图像形状相同的空数组来存储标记
    markers = np.zeros(distance_transform.shape, dtype=np.uint8)
    # 将局部最大值的位置标记为非零
    markers[coordinates[:, 0], coordinates[:, 1]] = range(len(coordinates))
    # 使用分水岭算法进行图像分割
    labels = watershed(-distance_transform, markers, mask=binary_image)
    # 创建一个空白图像
    blank_image = np.zeros(image.shape, dtype=np.uint8)
    # 绘制分水岭分割后的结果到空白图像上
    for label in np.unique(labels):
        if label == 0:
            continue
        # 创建一个与图像形状相同，但只有一个通道，数据类型为uint8的空数组作为mask
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        # 将label对应的区域标记为255
        mask[labels == label] = 255
        # 使用cv2.findContours找到mask中的轮廓
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # 使用cv2.drawContours将轮廓绘制到blank_image上
        cv2.drawContours(blank_image, contours, -1, (200, 200, 200), thickness=-1)
    # 计算对象像素和总像素
    object_pixels = np.sum(blank_image == 0)
    total_pixels = image.shape[0] * image.shape[1]
    # 计算并返回比例
    ratio = round((object_pixels / total_pixels) * 100, 3)
    if ratio > 50:
        print("wrong!")
        ratio = 50

    return ratio, blank_image

# 定义函数：转换、裁剪和计算对象比率
def convert_and_calculate_object_ratio(bmp_image_path, jpg_image_path):
    # 读取BMP图像
    image = cv2.imread(bmp_image_path, cv2.IMREAD_COLOR)
    # 裁剪图像
    image = image[:, 35:-85]
    image = image[0:-80, :]
    # 调整图像的亮度
    bright_image = cv2.convertScaleAbs(image, alpha=1, beta=0)
    # 显示原始图像和调整亮度后的图像；    #cv2.imshow('Original Image', image)；    #cv2.imshow('Bright Image', bright_image)；    #cv2.waitKey(1)；    #cv2.destroyAllWindows()
    image = bright_image
    # 保存裁剪后的图像为JPG格式
    cv2.imwrite(jpg_image_path, image)
    # 将图像从RGB转为灰度
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 对图像进行二值化处理
    _, thresholded_image = cv2.threshold(grayscale_image, 140, 255, cv2.THRESH_BINARY)
    # 保存二值化后的图像
    binary_image_path = bmp_image_path.replace('.bmp', '_binary.jpg')
    cv2.imwrite(binary_image_path, thresholded_image)
    # 计算对象像素和总像素
    object_pixels = np.sum(thresholded_image == 255)
    total_pixels = image.shape[0] * image.shape[1]
    # 计算比率
    ratio = round((object_pixels / total_pixels) * 100, 3)
    # 提取轮廓并计算比例
    contour_ratio, contour_image = extract_contour_and_calculate_ratio(image)
    # 保存轮廓图像
    contour_image_path = bmp_image_path.replace('.bmp', '_contour.jpg')
    cv2.imwrite(contour_image_path, contour_image)
    # 使用分水岭算法提取轮廓并计算比例
    watershed_ratio, watershed_image = extract_contour_and_calculate_ratio_watershed(image)
    # 保存分水岭图像
    watershed_image_path = bmp_image_path.replace('.bmp', '_watershed.jpg')
    cv2.imwrite(watershed_image_path, watershed_image)
    # 计算平均比例
    avg_ratio = round(((ratio + contour_ratio + watershed_ratio) / 3), 3)
    return ratio, contour_ratio, watershed_ratio, avg_ratio

# 定义函数：处理图像并计算比例
def process_images_and_calculate_ratios(directory_path):
    # 找到指定目录下所有的.bmp文件
    global ratio
    bmp_filenames = [f for f in os.listdir(directory_path) if f.endswith('.bmp')]
    # 创建一个空的DataFrame，用于存储计算结果
    df = pd.DataFrame(columns=['filename', 'object_ratio', 'contour_ratio', 'watershed_ratio', 'avg_ratio'])
    # 遍历所有.bmp文件
    for bmp_filename in bmp_filenames:
        # 将.bmp文件名转换为.jpg文件名
        jpg_filename = bmp_filename.replace('.bmp', '.jpg')
        # 构建.jpg和.bmp文件的完整路径
        jpg_image_path = os.path.join(directory_path, jpg_filename)
        bmp_image_path = os.path.join(directory_path, bmp_filename)
        # 调用convert_and_calculate_object_ratio函数处理图像并计算比例
        ratio, contour_ratio, watershed_ratio, avg_ratio = convert_and_calculate_object_ratio(bmp_image_path, jpg_image_path)
        # 将.jpg文件名的扩展名去掉
        jpg_filename_no_ext = jpg_filename.replace('.jpg', '')
        # 将计算结果添加到DataFrame中
        df = pd.concat([df, pd.DataFrame([{'filename': jpg_filename_no_ext, 'object_ratio': ratio, 'contour_ratio': contour_ratio, 'watershed_ratio': watershed_ratio, 'avg_ratio': avg_ratio}])], ignore_index=True)

        # 返回DataFrame
    return df




