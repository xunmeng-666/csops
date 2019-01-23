# -*- coding:utf-8-*-

import os

BASH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print('base',BASH)
export_file = os.path.join(BASH,'static/files/download/')
upload_img = os.path.join(BASH,'static/files/upload/img/')

