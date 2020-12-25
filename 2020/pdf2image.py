#!/usr/bin/python
# -*- coding:utf-8 -*-
__doc__ = "pdf批量转图片"

import os
import time
import fitz
import oss2
from PIL import Image
import traceback
from datetime import datetime
from requests import session
from urllib.parse import urlparse, unquote
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, TIMESTAMP, Float

try:
    from sqlalchemy.ext.declarative import declarative_base
except:
    from sqlalchemy.orm import declarative_base

s = session()

# oss生成链接过期时间
UrlTimeout = 24 * 60 * 60

# OSS配置
AccessKey_ID = "你的id"
AccessKeySecret = "你的密码"
OssHost = "你的oss"
OssBucket = "你的bucket"
OssPath = '你的oss文件路径/'
# mysql url
mysql_url = "mysql+pymysql://root:123456@127.0.0.1/camel_test?charset=utf8"
table_name = 'table_name'  # 数据库表名


class FileOss(object):
    def __init__(self, AccessKey_ID, AccessKeySecret, OssHost, OssBucket, OssPath, UrlTimeout):
        self.AccessKey_ID = AccessKey_ID
        self.AccessKeySecret = AccessKeySecret
        self.OssHost = OssHost
        self.OssBucket = OssBucket
        self.UrlTimeout = UrlTimeout
        self.OssPath = OssPath
        self.auth = oss2.Auth(self.AccessKey_ID, self.AccessKeySecret)
        self.bucket = oss2.Bucket(self.auth, self.OssHost, self.OssBucket)

    def upload(self, filename, file):
        """

        :param filename: 文件名称
        :param path:    文件储存路径
        :return:
        """
        self.bucket.put_object(self.OssPath + filename, file)
        exist = self.bucket.object_exists(self.OssPath + filename)
        if exist:
            return filename
        else:
            return None

    def file_exist(self, filename):
        exist = self.bucket.object_exists(self.OssPath + filename)
        return exist

    def sign_url(self, filename, expires):
        try:
            exist = self.bucket.object_exists(self.OssPath + filename)
            if exist:
                if expires:
                    url = self.bucket.sign_url('GET', self.OssPath + filename, expires)
                else:
                    url = self.bucket.sign_url('GET', self.OssPath + filename, self.UrlTimeout)
                return url
            else:
                return None
        except:
            return None

    def delete_file(self, filename):
        self.bucket.delete_object(self.OssPath + filename)

    def get_file(self, filename, path):
        self.bucket.get_object_to_file(self.OssPath + filename, path)


# 基础实例化
oss = FileOss(AccessKey_ID, AccessKeySecret, OssHost, OssBucket, OssPath, UrlTimeout)
engine = create_engine(mysql_url,
                       echo=False,
                       pool_size=8,
                       pool_recycle=1800
                       )
# 创建session
DbSession = sessionmaker(bind=engine)
session = DbSession()
Base = declarative_base()


class XXXXX(Base):
    __tablename__ = table_name
    plate = Column(String(8), primary_key=True, index=True)  # 车牌号码(主键)
    url_vrc = Column(String(512))  # 车辆登记证
    url_vrc_two = Column(String(512))  # 车辆登记证2
    vehicle_model = Column(String(25))  # 车辆型号  # 车辆型号
    url_vehicle_license = Column(String(512))  # 车辆行驶证
    url_voc = Column(String(512))  # 车辆道路运输证
    url_truck_jqx = Column(String(512))  # 交强保险单
    url_truck_syx = Column(String(512))  # 商业保险单
    car_lost_cost = Column(Float)  # 车辆损失险保险金额
    url_others_insurance = Column(String(512))  # 其他险保单
    create_at = Column(TIMESTAMP, default=datetime.now)  # 初次提交时间
    update_at = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)  # 更新时间


tk = XXXXX


class Pdf2Img:
    pdf = ".pdf"
    image = ".jpg"
    flag = ["_vrc", "url_vrc_two", "License_", "Voc_", "_jqx", "qx_", "ruck"]

    def __init__(self, root_path, mysql_url):
        self.path = root_path  # 本地pdf文件位置
        self.mysqlurl = mysql_url
        self.oss_path = self.path + OssPath  # oss图片下载存放位置
        self.remote_path = self.path + 'remote/'  # 远程图片下载存放位置
        if not os.path.exists(self.oss_path):
            print("mkdir {}".format(self.oss_path))
            os.makedirs(self.oss_path)
        if not os.path.exists(self.remote_path):
            print("mkdir {}".format(self.remote_path))
            os.makedirs(self.remote_path)
        self.auto_upload_oss = False
        self.update_db = False
        self.sql_list = []
        self.failed_list = []

    def walk_local_file(self, path):
        """多层目录"""
        allfile = []
        if not path:
            path = self.path
        for (root, dirs, files) in os.walk(path):
            for filename in files:
                filename = os.path.join(root, filename)
                if self.match_name(filename):
                    allfile.append(filename)
        return allfile

    def list_local_file(self, path=None):
        """遍历单个目录"""
        allfile = []
        if not path:
            path = self.path
        filenames = os.listdir(path)  # 获取PDF文件列表
        for filename in filenames:
            if self.match_name(filename):
                full_path = os.path.join(path, filename)  # 拼接，得到PDF文件的绝对路径
                allfile.append(full_path)
        return allfile

    def match_name(self, filename):
        """匹配文件名,复合条件则返回"""
        if not filename:
            return False
        if self.pdf not in filename:
            return False
        for x in self.flag:
            if x in filename:
                return True

    def mysql_query(self):
        """数据库查询需要转换的数据"""
        all_local_file = []  # 分拣两种文件
        all_oss_file = []
        flag = 'http'
        txt = 'url_vrc like "%.pdf%" or url_vrc_two like "%.pdf%" or url_vehicle_license like "%.pdf%" or ' \
              'url_voc like "%.pdf%" or url_truck_jqx like "%.pdf%" or url_others_insurance like "%.pdf%"'
        _obj = session.query(tk.url_vrc,
                             tk.url_vrc_two,
                             tk.url_vehicle_license,
                             tk.url_voc,
                             tk.url_truck_jqx,
                             tk.url_others_insurance,
                             tk.plate
                             ).filter(text(txt)).all()
        for item in _obj:
            if self.match_name(item.url_vrc):
                if flag in item.url_vrc:
                    all_local_file.append({'url_vrc': item.url_vrc})
                else:
                    all_oss_file.append({'url_vrc': item.url_vrc})
            if self.match_name(item.url_vrc_two):
                if flag in item.url_vrc_two:
                    all_local_file.append({'url_vrc_two': item.url_vrc_two})
                else:
                    all_oss_file.append({'url_vrc_two': item.url_vrc_two})
            if self.match_name(item.url_vehicle_license):
                if flag in item.url_vehicle_license:
                    all_local_file.append({'url_vehicle_license': item.url_vehicle_license})
                else:
                    all_oss_file.append({'url_vehicle_license': item.url_vehicle_license})
            if self.match_name(item.url_voc):
                if flag in item.url_voc:
                    all_local_file.append({'url_voc': item.url_voc})
                else:
                    all_oss_file.append({'url_voc': item.url_voc})
            if self.match_name(item.url_truck_jqx):
                if flag in item.url_truck_jqx:
                    all_local_file.append({'url_truck_jqx': item.url_truck_jqx})
                else:
                    all_oss_file.append({'url_truck_jqx': item.url_truck_jqx})
            if self.match_name(item.url_others_insurance):
                if flag in item.url_others_insurance:
                    all_local_file.append({'url_others_insurance': item.url_others_insurance})
                else:
                    all_oss_file.append({'url_others_insurance': item.url_others_insurance})
        return all_local_file, all_oss_file

    def mysql_update(self, data):
        """更新数据库中的数据"""
        key = list(data.keys())[0]
        value = list(data.values())[0]
        new_value = value.replace(self.pdf, self.image)
        stmt = 'update {} set {}="{}" where {}="{}";'.format(table_name, key, new_value, key, value)
        # print("stmt:", stmt)
        if not self.update_db:
            self.sql_list.append(stmt + os.linesep)
            return
        session.execute(stmt)
        session.commit()

    def download_file(self, url, path=None):
        """下载pdf文件到本地"""
        try:
            if not path:
                path = self.path
            response = s.get(url, timeout=10)
            url = unquote(urlparse(url).path)
            filename = str(url.split('/')[-1])
            fullpath = path + filename
            with open(fullpath, 'wb') as f:
                f.write(response.content)
            response.close()
            return filename, fullpath
        except Exception:
            traceback.print_exc()
            return None, None

    def local_work(self, fullpath):
        """本地文件转换"""
        print("--------local_work start----------")
        result = self.pdf2img(fullpath)
        print("--------local_work end----------")
        return result

    def remote_work(self, url, path=None):
        """远程转换"""
        print("--------remote_work start----------")
        if not path:
            path = self.remote_path
        filename, fullpath = self.download_file(url, path)
        result = self.pdf2img(fullpath)
        # todo 上传转换好的图片到远程服务器
        print("--------remote_work end----------")
        return result

    def oss_work(self, filename, path=None):
        """转换oss中的pdf文件为jpg"""
        print("--------oss_work start----------")
        if not path:
            path = self.oss_path
        if "#" in filename:
            filename = filename.split("#")[0]
        url = oss.sign_url(filename, UrlTimeout)
        if not url:
            print('not find {} in oss!'.format(filename))
            return
        _, fullpath = self.download_file(url, path=path)
        result = self.pdf2img(fullpath)
        if result and self.auto_upload_oss:
            new_name = filename.replace(self.pdf, self.image)
            with open(path + new_name, 'rb') as f:
                tmp = oss.upload(new_name, f.read())
                print("upload oss:", tmp)
        print("--------oss_work end----------")
        return result

    def work(self):
        """主函数"""
        all_local_file, all_oss_file = self.mysql_query()
        print("all_local_file:", all_local_file)
        print("all_oss_file:", all_oss_file)

        # 更新本地文件夹
        # for item in all_local_file:
        #     url = list(item.values())[0]
        #     filename = str(urlparse(url).path.split('/')[-1])
        #     if not os.path.exists(filename):
        #         continue
        #     fullpath = self.path + filename
        #     result = self.local_work(fullpath)
        #     if result:
        #         self.mysql_update(item)

        # 下载远程文件到本地,转化后手动上传
        for item in all_local_file:
            url = list(item.values())[0]
            filename = str(urlparse(url).path.split('/')[-1])
            if os.path.exists(filename):
                continue
            result = self.remote_work(url)
            if result:
                self.mysql_update(item)
            else:
                self.failed_list.append(url)

        # 下载oss文件到本地,转化后自动上传
        for item in all_oss_file:
            filename = list(item.values())[0]
            result = self.oss_work(filename)
            if result:
                self.mysql_update(item)
            else:
                self.failed_list.append(filename)
        print("-----------------------------------------")
        # 备份更新语句,手动执行
        if not self.update_db:
            with open(self.path + '/update_{}.sql'.format(table_name), 'w') as f:
                f.writelines(self.sql_list)
        # 备份更新语句,手动执行
        if self.failed_list:
            with open(self.path + '/failed_{}.log'.format(table_name), 'w') as f:
                for x in self.failed_list:
                    f.write(x + os.linesep)

    def pdf2img(self, fullpath):
        """转换程序,图片文件转换后会放在pdf文件同目录"""
        try:
            print("%s开始转换..." % fullpath)
            start_time = time.time()  # 开始时间
            # doc = fitz.Document(fullpath)  # 打开一个PDF文件，doc为Document类型，是一个包含每一页PDF文件的列表
            doc = fitz.open(fullpath, filetype="pdf")
            rotate = int(0)  # 设置图片的旋转角度
            zoom_x = 2.0  # 设置图片相对于PDF文件在X轴上的缩放比例
            zoom_y = 2.0  # 设置图片相对于PDF文件在Y轴上的缩放比例
            trans = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
            if doc.pageCount > 1:  # 获取PDF的页数
                img_list = []
                new_full_name = "%s%s" % (fullpath.split(".")[0], self.image)
                for pg in range(doc.pageCount):
                    page = doc[pg]  # 获得第pg页
                    pm = page.getPixmap(matrix=trans, alpha=False)  # 将其转化为光栅文件（位数）
                    tmp_full_name = "%s%s" % (new_full_name, pg)  # 保证输出的文件名不变
                    pm.writeImage(tmp_full_name)  # 将其输入为相应的图片格式，可以为位图，也可以为矢量图
                    img_list.append(tmp_full_name)
                if not merge_image(img_list, new_full_name):
                    return None
            else:
                page = doc[0]
                pm = page.getPixmap(matrix=trans, alpha=False)
                new_full_name = fullpath.split(".")[0]
                pm.writeImage("%s%s" % (new_full_name, self.image))
            end_time = time.time()  # 结束时间
            print('pdf2img时间=', end_time - start_time)
            print("%s转换完成！" % fullpath)
            return new_full_name
        except Exception:
            traceback.print_exc()
            return None


def merge_image(img_list, img_name):
    """拼接图片"""
    if img_list:
        name = img_list[0]
        color_mod = 'RGBA' if name.endswith('.png') else 'RGB'  # jpeg格式不支持RGBA
        first_img = Image.open(img_list[0])
        height_size = first_img.size[1]
        total_width = first_img.size[0]
        first_img.close()
        total_height = height_size * len(img_list)
        left = 0
        right = height_size
        target = Image.new(color_mod, (total_width, total_height))  # 最终拼接的图像的大小
        for img in img_list:
            tmp = Image.open(img).resize((total_width, height_size), Image.ANTIALIAS)  # 可能每页的图片分辨率不一样,强制转一下
            target.paste(tmp, (0, left, total_width, right))
            left += height_size
            right += height_size
        target.save(img_name, quality=100)
        for img in img_list:
            os.remove(img)
        return True
    else:
        return False


if __name__ == "__main__":
    path = "/home/pdf/"
    pdf = Pdf2Img(path, mysql_url)
    pdf.work()
