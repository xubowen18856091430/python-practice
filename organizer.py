import os
import shutil
from pathlib import Path

FILE_CATEGORIES = {
    "图片": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".ico"],
    "文档": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx", ".csv", ".md"],
    "视频": [".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv", ".webm"],
    "音频": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma"],
    "压缩包": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
    "程序": [".exe", ".msi", ".bat", ".sh", ".py", ".js", ".html", ".css", ".java", ".c", ".cpp"],
}

def get_category(suffix):
    suffix = suffix.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if suffix in extensions:
            return category
    return "其他"

def get_unique_path(dest_dir, filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    new_path = os.path.join(dest_dir, filename)
    while os.path.exists(new_path):
        new_path = os.path.join(dest_dir, f"{base}_{counter}{ext}")
        counter += 1
    return new_path

def plan_organize(folder):
    plans = []
    for item in folder.iterdir():
        if item.is_file() and item.name != os.path.basename(__file__):
            category = get_category(item.suffix)
            dest_dir = folder / category
            dest_path = Path(get_unique_path(str(dest_dir), item.name))
            plans.append((item, dest_path, category))
    return plans

def print_plans(plans):
    print(f"\n{'文件名':<30} {'将移入':<8}")
    print("-" * 42)
    for src, _, category in plans:
        print(f"{src.name:<30} {category}/")
    print(f"\n共预览 {len(plans)} 个文件待整理。")

def organize_folder(folder_path, preview=False):
    folder = Path(folder_path)
    if not folder.is_dir():
        print(f"错误：{folder_path} 不是有效的目录")
        return

    plans = plan_organize(folder)
    if not plans:
        print("没有需要整理的文件。")
        return

    print_plans(plans)
    if preview:
        return

    confirm = input("\n确认执行整理？(y/N): ").strip().lower()
    if confirm != "y":
        print("已取消。")
        return

    for src, dest_path, category in plans:
        dest_path.parent.mkdir(exist_ok=True)
        shutil.move(str(src), str(dest_path))
        print(f"已移动: {src.name} -> {category}/")

    print(f"\n整理完成！共移动了 {len(plans)} 个文件。")

def main():
    print("=" * 40)
    print("      文件夹自动整理工具")
    print("=" * 40)

    target = input("请输入要整理的文件夹路径（回车使用当前目录）: ").strip()
    if not target:
        target = os.getcwd()

    mode = input("选择模式：1=预览 + 确认整理  2=仅预览查看: ").strip()
    preview_only = mode == "2"

    organize_folder(target, preview=preview_only)

if __name__ == "__main__":
    main()
