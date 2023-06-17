# -*- coding: UTF-8 -*-
import json
import os

import qbittorrentapi


class RssManager:
    def __init__(self, conf_path: str) -> None:
        if os.path.exists(conf_path):
            with open(conf_path, "r", encoding="utf-8") as f:
                conf_info = json.load(f)
        else:
            print(f"Error, not found file: {conf_path}")
            return
        self.qbt_client = qbittorrentapi.Client(
            host=conf_info["qb_adress"],
            port=conf_info["qb_port"],
            username=conf_info["qb_user_name"],
            password=conf_info["qb_user_pwd"],
        )

        try:
            self.qbt_client.auth_log_in()
        except Exception as e:
            print(f"登录失败! {str(e)}")
            raise SystemExit("Login failed.")

        print(f"登录成功!")
        self.prompt()

    def get_rss_name_from_url(self, url: str):
        rss_item = self.qbt_client.rss_items()
        a = {}
        for i in rss_item.keys():
            if url == rss_item[i]["url"]:
                return i

    def prompt(self):
        rss_rule = self.qbt_client.rss_rules()
        rss_rule_list = list(rss_rule.keys())

        print(
            "\n".join(
                [
                    f"[{idx + 1}] {rule_name}"
                    for idx, rule_name in enumerate(rss_rule_list)
                ]
            )
        )
        print("删除订阅会同时删除RSS下载规则、对应的分类、对应的Torrent,并不会删除文件。")
        input_num = input("输入数字进行删除：")
        index = int(input_num) - 1
        rule_name = rss_rule_list[index]
        rule = rss_rule[rule_name]
        # print(rule)
        item_path = rule["savePath"]
        # print(item_path)
        category = rule["assignedCategory"]
        # print(category)
        feed_url = rule["affectedFeeds"][0]
        # print(feed_url)
        feed_name = self.get_rss_name_from_url(feed_url)
        # print(feed_name)

        # delete
        self.qbt_client.rss_remove_rule(rule_name)
        self.qbt_client.rss_remove_item(feed_name)
        a_t = self.qbt_client.torrents_info(category=category)
        torrent_hash_list = [torrent["hash"] for torrent in a_t]
        self.qbt_client.torrents_delete(torrent_hashes=torrent_hash_list)
        self.qbt_client.torrents_remove_categories(category)


if __name__ == "__main__":
    RssManager("rss_config.json")
