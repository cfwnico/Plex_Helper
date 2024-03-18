import os
import sys
import time
import traceback
from glob import escape, glob
from itertools import chain
from typing import List, Tuple


def get_workdir(arg_list: List[str]) -> str:
    """通过系统参数获得文件夹路径。
    若存在传入路径参数则优先返回路径文件所在的文件夹。
    其余情况则返回该程序运行所在的文件夹。
    如果传入多个路径参数则返回None。"""
    if len(arg_list) > 2:
        raise ValueError(f"传入参数过多")
    # 判断和获取绝对路径
    path = sys.argv[-1]
    try:
        path = os.path.realpath(path, strict=True)
    except OSError as e:
        print(f"传入路径无效：{path}")
        raise ValueError(f"传入路径无效：{path}") from e

    if os.path.isfile(path):
        path = os.path.dirname(path)
    return path


def get_filepath_list(path: str, ext_list: List[str]):
    """返回指定路径下包含指定后缀名的文件路径的列表。\n
    path: 路径参数。\n
    ext_list[str]: 包含后缀名的列表，例如[".mp4",".mkv"]。\n
    注意：如果没有找到对应的后缀名文件，则会返回一个空列表。
    """
    return sorted(
        list(chain(*[glob(os.path.join(escape(path), f"*{ext}")) for ext in ext_list]))
    )


def del_tc_ass_file(dir_path: str):
    """删除目录下的繁体字幕文件。"""
    if len(get_filepath_list(dir_path, [".ass", ".srt"])) == 0:
        return
    print("选择需要删除的字幕所包含的字符串：")
    print("1.tc.ass 2.TC.ass 3.cht.ass 4.自定义请直接输入，直接回车键跳过")
    ext_list = ["tc.ass", "TC.ass", "cht.ass"]
    i = input()
    if i.isnumeric():
        i = int(i)
        ext = ext_list[i - 1]
        for i in get_filepath_list(dir_path, [ext]):
            os.remove(i)
    else:
        if i != "":
            for i in get_filepath_list(dir_path, i):
                os.remove(i)


def get_bangumi_info() -> Tuple[str, str, int]:
    print("请输入剧集名称：")
    bangumi_name = input("")
    bangumi_name = bangumi_name.replace(":", "：")

    print("请输入季度：默认01")
    season_idx = input("")
    if season_idx == "":
        season_idx = "01"
    else:
        season_idx = f"{season_idx:0>2}"

    print("请输入开始集数：默认1")
    user_input = input("")
    if user_input == "":
        start_idx = 1
    else:
        start_idx = int(user_input)
    print(f"剧集名：{bangumi_name} 季度：{season_idx} 开始集： {start_idx}")
    return bangumi_name, season_idx, start_idx


def rename_files(
    media_file_list: List[str],
    dir_path: str,
    bangumi_name: str,
    season_idx: str,
    start_idx: int,
) -> None:
    # 计算媒体文件新旧文件名对应关系
    media_rename_list: List[Tuple[str, str]] = []
    for idx, file_name in enumerate(media_file_list):
        f_ext = os.path.splitext(file_name)[1]
        new_f_name = f"{bangumi_name} S{season_idx}E{start_idx + idx:0>2}{f_ext}"
        new_f_path = os.path.join(dir_path, new_f_name)
        media_rename_list.append((file_name, new_f_path))

    # 输出新旧文件名对比，并检测X.5总集篇
    print("即将进行如下规则的重命名：")
    for f, new_f in media_rename_list:
        f_name = os.path.basename(f)
        if ".5" in f_name:
            print("检测到文件名包含 *.5 ！")
        new_f_name = os.path.basename(new_f)
        print(f"{f_name} -> {new_f_name}")
    input("按下任意键开始重命名，退出请直接关闭程序。")

    # 创建log文件，可以通过log文件进行逆重命名。
    # log_path = os.path.join(dir_path, "rename_log.log")
    # with open(log_path, "a", encoding="utf-8") as ff:
    #     ff.write(
    #         "\n".join(
    #             [f"{old_name}\t{new_name}" for old_name, new_name in media_rename_list]
    #         )
    #     )

    # 重命名文件
    for f, f_new in media_rename_list:
        if f != f_new:
            os.rename(f, f_new)


def rename_media_file(dir_path: str):
    # 遍历媒体文件并获取路径
    media_ext_list = [".mkv", ".mp4"]
    media_file_list = get_filepath_list(dir_path, media_ext_list)
    if len(media_file_list) == 0:
        print("该文件夹下没有检测到媒体文件！")
        print("检测后缀：", media_ext_list)
        return

    # 输入重命名相关信息
    print(media_file_list[0])
    bangumi_name, season_idx, start_idx = get_bangumi_info()

    print("重命名媒体文件中...")
    rename_files(media_file_list, dir_path, bangumi_name, season_idx, start_idx)

    # 遍历字幕文件并获取路径
    ass_ext_list = [".ass", ".srt"]
    ass_file_list = get_filepath_list(dir_path, ass_ext_list)
    if len(ass_file_list) == 0:
        print("该文件夹下没有检测到字幕文件！")
        print("检测后缀：", ass_ext_list)
        return bangumi_name, season_idx

    print("重命名字幕文件中...")
    rename_files(ass_file_list, dir_path, bangumi_name, season_idx, start_idx)
    return bangumi_name, season_idx


if __name__ == "__main__":
    print("Plex Renamer v0.1 by:cfw")
    try:
        work_dir = get_workdir(sys.argv)
        print("文件夹路径：", work_dir)
        del_tc_ass_file(work_dir)
        re = rename_media_file(work_dir)
        # 重命名媒体文件夹
        new_dirpath = os.path.join(os.path.split(work_dir)[0], re[0])
        if work_dir != new_dirpath:
            print("即将重命名文件夹名称！退出请直接关闭。")
            print(new_dirpath)
            input("")
            os.rename(work_dir, new_dirpath)
        if int(re[1]) > 1:
            os.makedirs(os.path.join(new_dirpath, f"S{re[1]}"))
        print("处理完毕！即将退出！")
        time.sleep(4)
    except Exception as e:
        print(f"运行错误，请检查：{e}")
        traceback.print_exc()
        input()
