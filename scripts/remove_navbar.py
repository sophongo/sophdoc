from PIL import Image
import numpy as np
import os
from multiprocessing import Pool, cpu_count


def detect_navbar_height(image):
    """Detects the height of the navbar based on average row intensity."""
    gray_image = image.convert("L")
    image_np = np.array(gray_image)
    row_intensity = np.mean(image_np, axis=1)

    split_index = None
    for i in range(1, len(row_intensity)):
        if row_intensity[i] > 200:  # 阈值可根据实际情况调整
            split_index = i
            break
    return split_index


def add_border(image, border_color=(200, 200, 200)):
    """Adds a 1-pixel light gray border to the image."""
    border_size = 1
    new_width = image.width + 2 * border_size
    new_height = image.height + 2 * border_size

    # 创建一个新图像，填充为边框颜色
    bordered_image = Image.new("RGB", (new_width, new_height), border_color)
    # 将原始图像粘贴到新的图像中，居中
    bordered_image.paste(image, (border_size, border_size))
    return bordered_image


def process_image(args):
    """Processes a single image: removes navbar and adds border."""
    image_path, output_path = args
    try:
        image = Image.open(image_path)
        if image.mode != "RGB":
            image = image.convert("RGB")
        split_index = detect_navbar_height(image)

        if split_index is not None:
            cropped_image = image.crop((0, split_index, image.width, image.height))
            # 添加1像素淡灰色边框
            bordered_image = add_border(cropped_image)
            bordered_image.save(output_path)
            print(f"已成功处理并添加边框: {image_path}, 保存到: {output_path}")
        else:
            print(f"未检测到导航栏: {image_path}")
            # 即使未检测到导航栏，也添加边框
            bordered_image = add_border(image)
            bordered_image.save(output_path)
            print(f"已为未修改的图片添加边框: {image_path}, 保存到: {output_path}")

    except Exception as e:
        print(f"处理图片 {image_path} 时出错: {e}")


def batch_process(input_dir, output_dir):
    """Batch processes images in a folder to remove navbars and add borders using multiprocessing."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 获取所有需要处理的图片路径
    image_files = [
        filename
        for filename in os.listdir(input_dir)
        if filename.lower().endswith((".png", ".jpg", ".jpeg"))
    ]

    # 构建要处理的图片路径列表
    tasks = [
        (os.path.join(input_dir, filename), os.path.join(output_dir, filename))
        for filename in image_files
    ]

    if tasks:
        # 使用多进程池进行并行处理
        pool_size = min(cpu_count(), len(tasks))  # 不要创建多于需要的进程数
        with Pool(processes=pool_size) as pool:
            pool.map(process_image, tasks)
    else:
        print(f"文件夹 {input_dir} 中没有找到符合条件的图片。")


def find_images_dirs(root_dir):
    """Finds and returns a list of paths of 'images' directories within the given root directory."""
    images_dirs = []
    for dirpath, dirnames, _ in os.walk(root_dir):
        if "images" in dirnames:
            images_dir_path = os.path.join(dirpath, "images")
            images_dirs.append(os.path.relpath(images_dir_path, root_dir))
    return images_dirs


if __name__ == "__main__":
    root_directory = "docs"
    images_dirs = find_images_dirs(root_directory)
    if not images_dirs:
        print("未找到任何包含 'images' 文件夹的目录。")
    else:
        for folder in images_dirs:
            images_folder = os.path.join(root_directory, folder)
            print(f"正在处理文件夹: {images_folder}")
            batch_process(input_dir=images_folder, output_dir=images_folder)
        print("所有图片处理完成。")
