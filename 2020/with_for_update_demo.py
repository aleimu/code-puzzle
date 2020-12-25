__doc__ = "with_for_update 测试"

import time
import traceback
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, TIMESTAMP, Float

try:
    from sqlalchemy.ext.declarative import declarative_base
except:
    from sqlalchemy.orm import declarative_base

mysql_url = "mysql+pymysql://root:ptdAChu+byhzq2dCc0&MLd@127.0.0.1/camel_test?charset=utf8"
table_name = 'trucks_pdf'  # 上线时修改为trucks

engine = create_engine(mysql_url,
                       echo=True,
                       pool_size=8,
                       pool_recycle=1800
                       )
# 创建session
DbSession = sessionmaker(bind=engine)
session = DbSession()
Base = declarative_base()


class ShipperTrucks(Base):
    __tablename__ = table_name  # 承运商车辆表
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


tk = ShipperTrucks

plate = "云A13D57"


def test1():
    # _obj = session.query(tk).filter(tk.plate == plate).with_for_update().first()
    _obj = session.query(tk).filter(tk.plate == plate).first()
    print(_obj.plate)
    _obj.url_vrc = "333333333333"
    time.sleep(30)
    print(_obj.url_vrc)
    session.commit()


def test2():
    _obj = session.query(tk).filter(tk.plate == plate).with_for_update().first()
    print(_obj.url_vrc)


if __name__ == "__main__":
    # test1()
    test2()
