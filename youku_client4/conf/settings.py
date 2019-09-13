import os
# 文件的环境配置

BASE_PATH = os.path.dirname(os.path.dirname(__file__))

LOCAL_MOVIE_PATH = os.path.join(BASE_PATH,'local_movie')

DOWNLOAD_MOVIE = os.path.join(BASE_PATH,'download_movie')
