# Plex_Helper
为了方便使用plex而写的python程序。
# Plex_ReNamer.py
传入路径，将路径下媒体文件及字幕文件重命名为Plex所约定的命名。    
### 使用方法:  
1.拖拽**文件夹**或者**文件夹下的一个文件**到该py文件上。  
2.根据提示输入`剧集名称`与`季度数`及`开始集数`(如果不输入则使用默认文本)，  
3.程序会自动将媒体文件和对应的字幕文件重命名为Plex约定的媒体文件名格式。  
4.可选是否重命名文件夹。    

重命名后的媒体文件: `Ani S01E01.mkv…… ；Ani S01E01.ass……`  

支持的媒体文件格式:`mkv\mp4`  
支持的字幕文件格式:`ass\srt`  
# Mux_MKV_ASS.py
使用ffmpeg将外挂ass字幕文件混流进mkv文件。  
`目前该代码运行会消耗大量IO，暂时没找到更好的写法。`
# Rss_Rule_Set.py
通过qbittorrentapi库操作QB的WEBUI，自动设置RSS订阅及RSS订阅自动下载规则，省去手动管理。
注意：目标QB的运行环境仅限定Linux环境。  
### 主要依赖：
qbittorrent-api  
`pip install qbittorrent-api`
### 使用方法：
首次运行会自动创建一个配置文件，需要手动修改配置文件中的用户名及密码配置。
```
"qb_adress": "QB WEBUI的域名", 
"qb_port": 端口号, 
"qb_user_name": "用户名", 
"qb_user_pwd": "密码", 
"qb_save_path": "RSS自动下载的存储路径"
```  
自行修改配置文件后，修改程序的`130-141`行，再次运行程序，根据提示进行操作即可。
# Rss_Manage.py
管理QB的RSS订阅和自动下载规则。
### 使用方法：
启动程序后，程序后自动读取`Rss_Rule_Set.py`所创建的配置文件，之后根据序号输入需要删除的RSS订阅即可。
该程序会删除指定的RSS的订阅规则、RSS订阅自动下载规则、对应的QB分类、对应的Torrent任务。**不会删除任何磁盘文件。**