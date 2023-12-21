import cv2
import numpy as np
from skimage.segmentation import slic
from skimage.segmentation import mark_boundaries

from test_v2 import process_images_and_calculate_ratios


# 定义一个函数，用来提取图片的轮廓并保存
def extract_contour(image_path, output_path):
    # 加载图片
    image = cv2.imread(image_path)

    # 使用SLIC算法进行图像分割
    segments = slic(image, n_segments=5000, sigma=10)

    # 使用Canny算法获取轮廓
    edges = cv2.Canny(image, 30, 200)

    # 使用膨胀操作增强轮廓线
    dilated = cv2.dilate(edges, None)

    # 保存轮廓图片
    cv2.imwrite(output_path, dilated)

# 使用函数提取轮廓并保存
extract_contour('/home/sxwang/SOTAtest/test/20231212_164251512.bmp', '/home/sxwang/SOTAtest/test/20231212_164251512A.bmp')

