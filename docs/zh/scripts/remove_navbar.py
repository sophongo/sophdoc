from PIL import Image
import numpy as np
import os


def detect_navbar_height(image):
    """Detects the height of the navbar based on average row intensity."""
    # ... (与之前版本相同)


def remove_navbar(image_path):
    """Removes the navbar from an image and overwrites the original file."""
    try:
        image = Image.open(image_path)
        split_index = detect_navbar_height(image)

        if split_index:
            cropped_image = image.crop((0, split_index, image.width, image.height))
            cropped_image.save(image_path)  # 直接保存到原始路径
            print(f"已成功处理图片: {image_path}")
        else:
            print(f"未检测到导航栏: {image_path}")

    except Exception as e:
        print(f"处理图片 {image_path} 时出错: {e}")


def batch_process(input_dir):
    """Batch processes images in a folder to remove navbars."""

    for filename in os.listdir(input_dir):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(input_dir, filename)
            remove_navbar(image_path)


if __name__ == "__main__":
    image_folder = "docs/images"

    batch_process(input_dir=image_folder)
