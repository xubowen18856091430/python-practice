import os
import shutil
from pathlib import Path


FILE_CATEGORIES = {
    "图片": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".ico"],
    "文档": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx", ".csv", ".md"],
    "视频": [".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv", ".webm"],
    "音频": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma"],
    "压缩包": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
    "程序": [".exe", ".msi", ".bat", ".sh", ],
    "代码文件":[".py",".html",".css",".c",".java",".cpp",".js"],
}

def get_category(suffix):
    # TODO: 把 suffix 转小写
    # TODO: 遍历 FILE_CATEGORIES.items()，拿到 (分类名, 扩展名列表)
    # TODO: 如果 suffix 在扩展名列表里，return 分类名
    # TODO: 循环结束都没找到，return "其他"
    suffix=suffix.lower()
    for category,extensions in FILE_CATEGORIES.items():
        if suffix in extensions:
            return category
    return"其他"

def get_unique_path(dest_dir, filename):
    # TODO: 用 os.path.splitext(filename) 拆出 base 和 ext
    # TODO: counter = 1
    # TODO: new_path = os.path.join(dest_dir, filename)
    # TODO: while os.path.exists(new_path):
    #         new_path = os.path.join(dest_dir, f"{base}_{counter}{ext}")
    #         counter += 1
    # TODO: return new_path
    base,ext=os.path.splitext(filename)
    counter=1
    new_path=os.path.join(dest_dir,filename)
    while os.path.exists(new_path):
        new_path=os.path.join(dest_dir,f"{base}_{counter}{ext}")
        counter+=1
    return new_path

def plan_organize(folder):
    plans = []
    # TODO: for item in folder.iterdir():
    #         如果 item.is_file() 并且 item.name != os.path.basename(__file__):
    #             category = get_category(item.suffix)
    #             dest_dir = folder / category
    #             dest_path = Path(get_unique_path(str(dest_dir), item.name))
    #             plans.append((item, dest_path, category))
    for item in folder.iterdir():
        if item.is_file() and item.name !=os.path.basename(__file__):
            category=get_category(item.suffix)
            dest_dir=folder/category
            dest_path=Path(get_unique_path(str(dest_dir),item.name))
            plans.append((item,dest_path,category))
    return plans

def print_plans(plans):
    # TODO: 打印表头 "文件名" 和 "将移入"（用 f-string 左对齐）
    # TODO: for src, _, category in plans: 打印 src.name 和 category + "/"
    # TODO: 打印 "共预览 N 个文件"
    print(f"\n{'文件名':<30} {'将移入':<8}")
    print("-"*42)
    for src,_,category in plans:
        print(f"{src.name:<30} {category}/")
    print(f"\n共预览{len(plans)} 个文件")

def organize_folder(folder_path, preview=False):
    folder = Path(folder_path)
    # TODO: 如果 not folder.is_dir()，打印错误并 return
    if not folder.is_dir():
        print(f"错误{folder_path}不是有效目录！")
        return
    plans = plan_organize(folder)
    # TODO: 如果 not plans，打印"没有需要整理的文件"并 return
    if not plans:
        print("没有需要整理的文件。")
        return

    print_plans(plans)
    # TODO: 如果 preview，直接 return
    # TODO: confirm = input("确认执行整理？(y/N): ").strip().lower()
    # TODO: 如果 confirm != "y"，打印"已取消"并 return
    # TODO: for src, dest_path, category in plans:
    #         dest_path.parent.mkdir(exist_ok=True)
    #         shutil.move(str(src), str(dest_path))
    #         打印"已移动: ..."
    # TODO: 打印"整理完成！共移动了 N 个文件"
    if preview:
        return

    confirm=input("确认执行整理？(y/N): ").strip().lower()
    if confirm!='y':
        print("已取消")
        return
    for src,dest_path,category in plans:
        dest_path.parent.mkdir(exist_ok=True)
        shutil.move(str(src),str(dest_path))
        print(f"已移动:{src.name}->{category}")

    print(f"\n整理完成！共移动了{len(plans)}个文件")

def main():
    # TODO: 打印标题（=号分隔线 + "文件夹自动整理工具"）
    # TODO: target = input("请输入要整理的文件夹路径（回车使用当前目录）: ").strip()
    # TODO: 如果 not target，target = os.getcwd()
    # TODO: mode = input("选择模式：1=预览+确认整理  2=仅预览查看: ").strip()
    # TODO: preview_only = (mode == "2")
    # TODO: organize_folder(target, preview=preview_only)
    print("="*40)
    print("     文件夹自动整理工具")
    print("="*40)
    target=input("请输入要整理的文件夹路径(回车使用当前目录): ").strip()
    if not target:
        target=os.getcwd()
    mode=input("选择模式：1=预览+确认整理 2=仅预览查看： ").strip()
    preview_only=(mode=="2")
    organize_folder(target,preview=preview_only)
if __name__ == "__main__":
    main()
