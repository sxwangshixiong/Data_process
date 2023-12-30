import cv2
import os

# 图片路径
# dir_path = '/media/sxwang/Extreme SSD/1229/MightyOutput/20231229_174916/20231229_175040969/raw_images'
# out_dir_path = '/media/sxwang/Extreme SSD/1229/MightyOutput/20231229_174916/20231229_175040969/raw_image'
dir_path = '/home/sxwang/SOTAtest/231219MightyOutput/20231219_133013/20231219_135601721/raw_images'
out_dir_path = '/home/sxwang/SOTAtest/231219MightyOutput/20231219_133013/20231219_135601721/raw_images'
if not os.path.exists(out_dir_path):
    os.makedirs(out_dir_path)

# 遍历路径下的所有图片
for filename in os.listdir(dir_path):
    if filename.endswith('.bmp'):
        # 读取图片

        image = cv2.imread(os.path.join(dir_path, filename))
        # 将图片保存为jpg
        cv2.imwrite(os.path.join(out_dir_path, filename[:-4] + 'T.jpg'), image)
        if filename.endswith('.bmp'):
            os.remove(os.path.join(dir_path, filename))
