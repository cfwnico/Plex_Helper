# -*- coding: UTF-8 -*-
import json
import os
import sys
import xml.etree.ElementTree as ET

import qbittorrentapi
import requests


def load_config(conf_path: str) -> dict:
    if os.path.exists(conf_path):
        with open(conf_path, "r", encoding="utf-8") as f:
            conf_dict = json.load(f)
    else:
        create_config(conf_path)
        with open(conf_path, "r", encoding="utf-8") as f:
            conf_dict = json.load(f)
    return conf_dict


def create_config(conf_path: str):
    conf_dict = {
        "qb_adress": "127.0.0.1",
        "qb_port": 8080,
        "qb_user_name": "admin",
        "qb_user_pwd": "adminadmin",
        "qb_save_path": "/home/downloads/",
    }
    with open(conf_path, "w", encoding="utf-8") as f:
        json.dump(conf_dict, f, ensure_ascii=False)


def get_feed_title(feed_url: str):
    proxies = {"http": "http://127.0.0.1:10800", "https": "http://127.0.0.1:10800"}
    # 如果想使用代理来获取订阅标题，则使用下一行语句，注释下下行语句
    # r = requests.get(feed_url, proxies=proxies)
    r = requests.get(feed_url)
    root = ET.fromstring(r.text)
    rss_title = root[0][0].text
    return rss_title


def get_qb_client(conf_dict: dict):
    qbt_client = qbittorrentapi.Client(
        host=conf_dict["qb_adress"],
        port=conf_dict["qb_port"],
        username=conf_dict["qb_user_name"],
        password=conf_dict["qb_user_pwd"],
    )
    print(f"正在登录...请稍后...")
    print(f"webui地址：{conf_dict['qb_adress']}")
    print(f"用户名：{conf_dict['qb_user_name']}")
    try:
        qbt_client.auth_log_in()
        print(f"登录成功！")
        print(f"qBittorrent: {qbt_client.app.version}")
        print(f"qBittorrent Web API: {qbt_client.app.web_api_version}")
    except qbittorrentapi.LoginFailed as e:
        print(e)
        return
    return qbt_client


def rss_rule_set(
    qbt_client,
    conf_dict: dict,
    bangumi_name: str,
    feed_url: str,
    must_not_contain: str,
    romaji: str,
):
    save_path = os.path.join(conf_dict["qb_save_path"], romaji)
    rule = {
        "enable": True,
        "mustContain": bangumi_name,
        "mustNotContain": must_not_contain,
        "useRegx": True,
        "episodeFilter": "",
        "smartFilter": False,
        "previouslyMatchedEpisodes": [],
        "affectedFeeds": [feed_url],
        "ignoreDays": 0,
        "lastMatch": "",
        "addPaused": False,
        "assignedCategory": bangumi_name,
        "savePath": save_path,
    }
    print("番剧名称(必须包含)：")
    print(bangumi_name)
    print("订阅地址：")
    print(feed_url)
    print("忽略下载的文件所包含的字符：")
    print(must_not_contain)
    print("番剧存储文件夹：")
    print(save_path)
    input("请确认订阅信息!按下Enter确定!")
    qbt_client.torrents_create_category(bangumi_name)
    qbt_client.rss_add_feed(feed_url, get_feed_title(feed_url))
    qbt_client.rss_set_rule(rule_name=bangumi_name, rule_def=rule)


if __name__ == "__main__":
    conf_dict = load_config("rss_config.json")
    qbt_client = get_qb_client(conf_dict)
    if qbt_client is None:
        input("登录失败！请检查配置文件及网络环境！")
        sys.exit()
    # =======================================================================
    # 番剧名称、同时也是RSS自动下载中“必须包含”的字
    bangumi_name = "我推的孩子"
    # 番剧罗马音，下载的番剧存储的文件夹名称，同时方便刮削元数据
    romaji = "Oshi no Ko"
    # 订阅网址
    feed_url = "https://mikanime.tv/RSS/Bangumi?bangumiId=2995&subgroupid=552"
    # RSS自动下载中“不可包含”的字
    # must_not_contain = "720|CHT|繁体|B-Global|BIG5"
    must_not_contain = ""
    # =======================================================================

    rss_rule_set(
        qbt_client, conf_dict, bangumi_name, feed_url, must_not_contain, romaji
    )
