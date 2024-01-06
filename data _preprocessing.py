import cv2
import os

# 图片路径

dir_path = '/media/sxwang/DATA/SOTAtest/240103MightyOutput/20240103_114203/20240103_114312059/raw_image_s'
out_dir_path = '/media/sxwang/DATA/SOTAtest/240103MightyOutput/20240103_114203/20240103_114312059/raw_images'
if not os.path.exists(out_dir_path):
    os.makedirs(out_dir_path)

# 遍历路径下的所有图片
for filename in os.listdir(dir_path):
    if filename.endswith('.jpg'):
        # 读取图片

        image = cv2.imread(os.path.join(dir_path, filename))
        # 将图片保存为jpg
        cv2.imwrite(os.path.join(out_dir_path, filename[:-4] + 'T.jpg'), image)
        # if filename.endswith('.jpg'):
        #     os.remove(os.path.join(dir_path, filename))
