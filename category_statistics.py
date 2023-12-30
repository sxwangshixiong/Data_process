import cv2
import os
import pandas as pd

# 全局变量
coords = []
categories = ['pcb', 'rubber', 'tube', 'wire', 'can', 'painted_metal']
# colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255)]
colors = [(152, 223, 138), (196, 156, 148), (255, 152, 150), (197, 176, 213), (255, 187, 120), (174, 199, 232)]
# colors = [(44, 160, 44), (140, 86, 75), (214, 39, 40), (148, 103, 189), (255, 127, 14), (31, 119, 180)]
counts = {category: 0 for category in categories}

def click_event(event, x, y, flags, param):
    global counts, category
    if event == cv2.EVENT_LBUTTONDOWN:
        coords.append((x, y))
        cv2.circle(param, (x, y), 5, colors[categories.index(category)], -1)
        counts[category] += 1
        for idx, cat in enumerate(categories):
            cv2.rectangle(param, (10, 0), (1270, 30), (100, 100, 100), -1)
            for idx, cat in enumerate(categories):
                cv2.putText(param, f"{cat}: {counts[cat]}", (10 + 180 * idx, 25), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            colors[categories.index(cat)], 2)


def draw_rectangle_and_save(images_path, images_path_out, image_range):
    filenames = sorted(os.listdir(images_path))

    for filename in filenames:
        image = cv2.imread(os.path.join(images_path, filename))
        if image is None:
            print(f"无法读取图像：{filename}")
            continue

        cv2.rectangle(image, (0, image_range), (1280, 720), (0, 0, 255), 1)
        original_jpg_filename = filename.replace('T.jpg', '.jpg')
        cv2.imwrite(os.path.join(images_path_out, original_jpg_filename), image)

def annotate_objects_A(images_path_out):
    global counts, category
    df = pd.DataFrame(columns=['filename'] + categories)

    for filename in sorted(os.listdir(images_path_out)):
        if not filename.endswith('.bmp'):
            continue

        image = cv2.imread(os.path.join(images_path_out, filename))
        counts = {category: 0 for category in categories}

        for category in categories:
            cv2.rectangle(image, (10, 0), (1270, 30), (100, 100, 100), -1)
            cv2.namedWindow('Image')  # 创建窗口，然后设置回调
            cv2.setMouseCallback('Image', click_event, param=image)  # 将图像作为参数传递

            while True:
                cv2.rectangle(image, (0, 190), (1280, 720), colors[categories.index(category)], 2)
                for idx, cat in enumerate(categories):
                    cv2.putText(image, f"{cat}: {counts[cat]}", (10 + 180 * idx, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, colors[categories.index(cat)], 2)
                cv2.imshow('Image', image)
                if cv2.waitKey(1) & 0xFF == ord('n'):
                    cv2.rectangle(image, (0, 220), (1280, 720), (0, 0, 255), 2)
                    break

            # 每个类别后清除坐标列表
            coords.clear()

        # 所有类别后保存图像
        cv2.imwrite(os.path.join(images_path_out, filename), image)
        cv2.destroyAllWindows()
        df.loc[len(df)] = {**{'filename': filename.rstrip('.jpg')}, **counts}

    return df


def annotate_objects(images_path_out, image_range):
    global counts, category
    df = pd.DataFrame(columns=['filename'] + categories)

    filenames = sorted([f for f in os.listdir(images_path_out) if f.endswith('.jpg')])
    total_images = len(filenames)

    for idx, filename in enumerate(filenames):
        print(f"This is the {idx+1}th image out of {total_images} images.")

        image = cv2.imread(os.path.join(images_path_out, filename))
        counts = {category: 0 for category in categories}

        for category in categories:
            cv2.rectangle(image, (10, 0), (1270, 30), (100, 100, 100), -1)
            cv2.namedWindow('Image')  # 创建窗口，然后设置回调
            cv2.setMouseCallback('Image', click_event, param=image)  # 将图像作为参数传递

            while True:
                cv2.rectangle(image, (0, image_range), (1280, 720), colors[categories.index(category)], 2)
                for idx, cat in enumerate(categories):
                    cv2.putText(image, f"{cat}: {counts[cat]}", (10 + 180 * idx, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, colors[categories.index(cat)], 2)
                cv2.imshow('Image', image)
                if cv2.waitKey(1) & 0xFF == ord('n'):
                    cv2.rectangle(image, (0, image_range), (1280, 720), (0, 0, 255), 2)
                    break

            # 每个类别后清除坐标列表
            coords.clear()

        # 所有类别后保存图像
        cv2.imwrite(os.path.join(images_path_out, filename), image)
        cv2.destroyAllWindows()
        df.loc[len(df)] = {**{'filename': filename.rstrip('.jpg')}, **counts}

    return df


def category_statistics(images_path, image_range):

    new_folder_path = os.path.join(images_path + "/result")
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
    images_path_out = new_folder_path
    draw_rectangle_and_save(images_path, images_path_out, image_range)
    df = annotate_objects(images_path_out, image_range)
    df.to_excel(images_path + "/" + str(images_path)[-23:] + ".xlsx")
    print(df)


