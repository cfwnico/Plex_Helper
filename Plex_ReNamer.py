import json
import os
import sys
import traceback
from glob import glob


def get_root_dir():
    path = os.path.realpath(sys.argv[1])
    if os.path.isfile(path):
        root_dir = os.path.dirname(path)
    else:
        root_dir = path
    return root_dir


def proc_path(path: str):
    """处理glob函数路径中包含'[ ]'的情况，通过转义让glob不处理'[ ]'。\n
    path: 路径参数。"""
    newpath = ""
    for l in path:
        if l == "[":  # 处理'['
            l = "[[]"  # 转换成'[[]'
        elif l == "]":  # 处理']'
            l = "[]]"  # 转换成'[]]'
        else:  # 其余的保持不变
            l = l
        newpath = newpath + l  # 处理后的路径
    return newpath


def get_filepath_list(path: str, ext_list: list[str]):
    result_list = []
    for ext in ext_list:
        glob_path = proc_path(os.path.join(path, f"*{ext}"))
        result_list = glob(glob_path) + result_list
    return result_list


def del_tc_ass_file(dir_path: str):
    ass_file_list = get_filepath_list(dir_path, [".ass"])
    if len(ass_file_list) == 0:
        return
    print("选择需要删除的字幕所包含的字符串：")
    print("1.tc.ass 2.TC.ass 3.cht.ass 4.自定义")
    ext_list = ["tc.ass", "TC.ass", "cht.ass"]
    i = int(input(""))
    if i == 4:
        print("请输入字符串：")
        ext = input("")
    else:
        ext = ext_list[i - 1]
    for i in ass_file_list:
        file_name = os.path.basename(i)
        if ext in file_name:
            os.remove(i)


def rename_media_file(dir_path: str):
    media_file_list = get_filepath_list(dir_path, [".mkv", ".mp4"])
    if len(media_file_list) == 0:
        print(f"没有检测到媒体文件！")
        return
    else:
        print(media_file_list[0])

    print("请输入番剧罗马名：")
    bangumi_name = input("")
    print("请输入季度：")
    S_num = input("")

    media_file_list = sorted(media_file_list)
    new_media_file_list = []
    for i in range(len(media_file_list)):
        E_num = str(i + 1)
        if len(E_num) == 1:
            E_num = f"0{E_num}"
        ext = os.path.splitext(media_file_list[i])[1]
        new_media_file_name = f"{bangumi_name} S0{S_num}E{E_num}{ext}"
        new_media_file_path = os.path.join(dir_path, new_media_file_name)
        new_media_file_list.append(new_media_file_path)
    media_rename_list = list(zip(media_file_list, new_media_file_list))
    for m, n in media_rename_list:
        cur_name = os.path.basename(m)
        if ".5" in cur_name:
            print("检测到*.5总集篇！")
        new_name = os.path.basename(n)
        print(f"{cur_name} → {new_name}")
    input(f"按下任意键开始重命名媒体文件！退出请直接关闭。")
    input("注意：该操作不可撤销！")
    with open("media_rename.json", "w", encoding="utf-8") as f:
        json.dump(media_rename_list, f, ensure_ascii=False)
    for old_path, new_path in media_rename_list:
        if old_path != new_path:
            os.rename(old_path, new_path)
    season_dirpath = os.path.join(dir_path, f"S0{S_num}")
    if not os.path.exists(season_dirpath):
        os.mkdir(season_dirpath)

    ass_file_list = get_filepath_list(dir_path, [".ass"])
    if len(ass_file_list) == 0:
        print("没有检测到字幕文件！")
        return bangumi_name
    ass_file_list = sorted(ass_file_list)
    new_ass_file_list = []
    for i in range(len(ass_file_list)):
        E_num = str(i + 1)
        if len(E_num) == 1:
            E_num = f"0{E_num}"
        new_ass_file_name = f"{bangumi_name} S0{S_num}E{E_num}.ass"
        new_ass_file_path = os.path.join(dir_path, new_ass_file_name)
        new_ass_file_list.append(new_ass_file_path)
    ass_rename_list = list(zip(ass_file_list, new_ass_file_list))
    for m, n in ass_rename_list:
        cur_name = os.path.basename(m)
        new_name = os.path.basename(n)
        print(f"{cur_name} → {new_name}")
    input("按下任意键开始重命名字幕文件！退出请直接关闭。")
    input("注意：该操作不可撤销！")
    for old_path, new_path in ass_rename_list:
        if old_path != new_path:
            os.rename(old_path, new_path)
    return bangumi_name


def rename_media_dir(dir_path: str, bangumi_name: str):
    new_dirpath = os.path.join(os.path.split(dir_path)[0], bangumi_name)
    print("即将重命名文件夹名称！退出请直接关闭。")
    print(new_dirpath)
    input("")
    os.rename(dir_path, new_dirpath)


if __name__ == "__main__":
    try:
        root_dir = get_root_dir()
        del_tc_ass_file(root_dir)
        bangumi_name = rename_media_file(root_dir)
        input("处理完成！")
        if bangumi_name is not None:
            rename_media_dir(root_dir, bangumi_name)
    except Exception:
        with open("Plex_ReNamer_ErrorLog.txt", "w") as f:
            f.write(traceback.format_exc())
