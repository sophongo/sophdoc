import os
import re
import requests
from urllib.parse import urlparse
from pathlib import Path


def download_image(url, save_directory):
    """下载图片并保存到指定目录，返回保存的文件名"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        # 从URL解析出文件名
        parsed_url = urlparse(url)
        image_name = os.path.basename(parsed_url.path)
        # 如果文件名为空，使用默认名称
        if not image_name:
            image_name = "image.jpg"
        # 解决重名文件问题
        original_image_name = image_name
        counter = 1
        while os.path.exists(os.path.join(save_directory, image_name)):
            name, ext = os.path.splitext(original_image_name)
            image_name = f"{name}_{counter}{ext}"
            counter += 1
        # 保存图片
        with open(os.path.join(save_directory, image_name), "wb") as f:
            f.write(response.content)
        return image_name
    except Exception as e:
        print(f"下载图片失败：{url}，错误：{e}")
        return None


def replace_image_links(markdown_content, markdown_path, images_directory):
    """替换markdown内容中的图片链接，下载图片并更新链接"""
    # 匹配markdown图片链接的正则表达式
    image_pattern = r"!\[.*?\]\((http.*?)\)"
    matches = re.findall(image_pattern, markdown_content)
    updated_content = markdown_content
    for url in matches:
        print(f"处理图片：{url}")
        image_name = download_image(url, images_directory)
        if image_name:
            # 计算相对路径
            relative_path = os.path.relpath(
                os.path.join(images_directory, image_name),
                start=os.path.dirname(markdown_path),
            )
            # 更新markdown内容
            updated_content = updated_content.replace(url, relative_path)
    return updated_content


def process_markdown_files(root_directory, images_directory):
    """递归处理目录下的所有markdown文件"""
    for root, dirs, files in os.walk(root_directory):
        for file in files:
            if file.lower().endswith(".md"):
                markdown_path = os.path.join(root, file)
                print(f"处理文件：{markdown_path}")
                with open(markdown_path, "r", encoding="utf-8") as f:
                    content = f.read()
                updated_content = replace_image_links(
                    content, markdown_path, images_directory
                )
                if updated_content != content:
                    # 如果内容有更新，写回文件
                    with open(markdown_path, "w", encoding="utf-8") as f:
                        f.write(updated_content)


if __name__ == "__main__":
    docs_directory = "docs"
    images_directory = os.path.join(docs_directory, "images")
    # 创建images目录
    os.makedirs(images_directory, exist_ok=True)
    process_markdown_files(docs_directory, images_directory)
    print("所有文件处理完成。")
