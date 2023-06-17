import os
import shutil
import subprocess
import sys
from glob import glob


def get_work_dir():
    """返回传入的路径参数.如果传入的路径是文件则返回该文件所在的目录."""
    path = os.path.realpath(sys.argv[1])
    if os.path.isfile(path):
        root_dir = os.path.dirname(path)
    else:
        root_dir = path
    return root_dir


def new_glob(path: str):
    """重新封装glob函数,使glob不对方括号进行转义."""
    newpath = ""
    for l in path:
        if l == "[":  # 处理'['
            l = "[[]"  # 转换成'[[]'
        elif l == "]":  # 处理']'
            l = "[]]"  # 转换成'[]]'
        else:  # 其余的保持不变
            l = l
        newpath = newpath + l  # 处理后的路径
    return glob(newpath, recursive=True)


def get_filepath_list_from_ext(path: str, ext: str | list[str]):
    """返回路径下指定后缀名的文件的路径(遍历子目录).ext参数可接受一个包含多个后缀名的list.例如:[".mkv"]."""
    result_list = []
    if isinstance(ext, str):
        ext = [ext]
    for e in ext:
        result_list = new_glob(os.path.join(path, "**", f"*{e}")) + result_list
    return result_list


def mux_ass(mkv_file_path: str, out_dir: str):
    """查找同文件名的ass字幕文件并混流到输出文件夹."""
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    ass_file_path = os.path.splitext(mkv_file_path)[0] + ".ass"
    if not os.path.exists(ass_file_path):
        return
    out_file_path = os.path.join(out_dir, os.path.basename(mkv_file_path))
    cmd_str = [
        "ffmpeg",
        "-y",
        "-i",
        mkv_file_path,
        "-i",
        ass_file_path,
        "-c",
        "copy",
        "-metadata:s:s:0",
        "language=chi",
        "-metadata:s:s:0",
        "title=中文",
        out_file_path,
    ]
    re = subprocess.run(cmd_str)
    return_code = re.returncode
    if return_code == 0:
        return out_file_path
    else:
        return


if __name__ == "__main__":
    mkv_dir_path = get_work_dir()
    mkv_list = get_filepath_list_from_ext(mkv_dir_path, ".mkv")
    for mkv_path in mkv_list:
        out_file_path = mux_ass(mkv_path, "D:\Output")
        if out_file_path is not None:
            os.remove(mkv_path)
            ass_path = os.path.splitext(mkv_path)[0] + ".ass"
            os.remove(ass_path)
            print("正在移动:")
            print(out_file_path)
            print("         ↓         ")
            print(mkv_path)
            shutil.move(out_file_path, mkv_path)
