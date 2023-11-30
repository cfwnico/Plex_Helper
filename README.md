# Plex_Helper
为了方便使用plex而写的python程序.
# Plex_ReNamer.py
传入路径，将路径下媒体文件及字幕文件重命名为Plex所约定的命名.  
使用方法:  
拖拽文件夹或者一个文件到该py中,之后根据提示输入剧集名称与季度数及开始集数(如果不输入则使用默认文本),之后程序会自动将媒体文件和对应的字幕文件重命名为Plex约定的媒体文件名格式.之后可选是否重命名文件夹.    
例如: Ani S01E01.mkv;Ani S01E01.ass......  
支持的媒体文件格式:mkv\mp4
支持的字幕文件格式:ass\srt
# Mux_MKV_ASS.py
使用ffmpeg将外挂ass字幕文件混流进mkv文件.
目前代码写法需要消耗大量IO,暂时没找到更好的写法.
# Rss_Rule_Set.py
通过qbittorrentapi库操作QB的WEBUI，自动设置RSS订阅及RSS订阅自动下载规则，省去手动管理.
# Rss_Manage.py
管理QB的RSS订阅和自动下载规则.
