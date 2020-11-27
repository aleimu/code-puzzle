# -*- coding:utf-8 -*-

import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy, get_state
from sqlalchemy import text, Integer, CHAR, Column, DECIMAL, Date, DateTime, Float, ForeignKey, Index, LargeBinary, \
    String, TIMESTAMP, Table, Text, Time, TypeDecorator
from sqlalchemy.dialects.mysql import BIGINT, DATETIME, INTEGER, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.sql import exists, and_, text, or_
from sqlalchemy import create_engine

from flask_sqlalchemy import *


class RouterSQLAlchemy(SQLAlchemy):
    def use(self, bind):
        if bind:
            self.new_bind = bind
        return self

    def create_session(self, options):
        return orm.sessionmaker(class_=RouterSignallingSession, db=self, **options)


class RouterSignallingSession(SignallingSession):
    def get_bind(self, mapper=None, clause=None):
        if mapper is not None:
            info = getattr(mapper.mapped_table, 'info', {})
            bind_key1 = info.get('bind_key')
            print "-----bind_key1-----", bind_key1
            state = get_state(self.app)
            if hasattr(state.db, 'new_bind') and state.db.new_bind:
                bind_key2 = state.db.new_bind
                print "-----bind_key2-----", bind_key2  # 优先使用bind_key2
                if bind_key2:
                    return state.db.get_engine(self.app, bind=bind_key2)
                if bind_key1:
                    return state.db.get_engine(self.app, bind=bind_key1)
        return SessionBase.get_bind(self, mapper, clause)


read_dbname = "camel_test"
write_dbname = "camel_test_02"

SQLALCHEMY_DATABASE_URI = 'mysql://toto:toto123@127.0.0.1:3306/%s?charset=utf8' % read_dbname
WRITE_SQLALCHEMY_DATABASE_URI = 'mysql://toto:toto123@127.0.0.1:3306/%s?charset=utf8' % write_dbname

read_engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    echo=False,
    max_overflow=5)

write_engine = create_engine(
    WRITE_SQLALCHEMY_DATABASE_URI,
    echo=False,
    max_overflow=5)

app = Flask(__name__, instance_relative_config=True)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI  # 配置主库,防止意外
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_BINDS'] = {  # 此配置中的key应和db.set中参数保持一致,value为对应库的连接
    'read_db': SQLALCHEMY_DATABASE_URI,  # 读库
    'write_db': WRITE_SQLALCHEMY_DATABASE_URI  # 写库
}
db = RouterSQLAlchemy(app)


class Base(db.Model):
    __abstract__ = True

    @classmethod
    def use(self, bind):
        if bind:
            self.__table__.info['bind_key'] = bind
            self.__bind_key__ = bind
            db.use(bind)
        return self

    def to_dict(self):
        dict = {}
        dict.update(self.__dict__)
        if "_sa_instance_state" in dict:
            del dict['_sa_instance_state']
        return dict


class AdGroup(Base):
    __tablename__ = 'ad_group'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(64), nullable=False, index=True, doc='组名')
    status = Column(INTEGER(11), server_default=text("'1'"))
    note = Column(String(32))
    create_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), doc='创建时间')
    update_time = Column(TIMESTAMP)


class AdImage(Base):
    __tablename__ = 'ad_image'

    id = Column(INTEGER(11), primary_key=True)
    group_id = Column(INTEGER(11), doc='分组id :ad_group.id')
    image_name = Column(String(256), doc='图片名')
    image_url = Column(String(256), doc='图片存放链接')
    ad_url = Column(String(256), doc='广告链接')
    note = Column(String(32))
    status = Column(INTEGER(11), server_default=text("'1'"))
    create_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), doc='创建时间')
    update_time = Column(TIMESTAMP)


def read1():
    print '---read1----'
    print AdGroup.use('write_db').query.join(AdImage, AdImage.group_id == AdGroup.id).filter().first()
    print '-------default------------'
    print db.session.query(AdGroup, AdImage).join(AdImage, AdImage.group_id == AdGroup.id).first()
    print '---------write_db----------'
    print db.use("write_db").session.query(AdGroup, AdImage).join(AdImage,
                                                                  AdImage.group_id == AdGroup.id).first()
    print '--------read_db-----------'
    print  db.use("read_db").session.query(AdGroup, AdImage).join(AdImage,
                                                                  AdImage.group_id == AdGroup.id).first()
    print '-------default------------'
    print db.session.query(AdGroup, AdImage).join(AdImage, AdImage.group_id == AdGroup.id).first()
    print '---------write_db----------'
    print db.use("write_db").session.query(AdGroup, AdImage).join(AdImage,
                                                                  AdImage.group_id == AdGroup.id).first()


def read2():
    print '---read2----', AdGroup, issubclass(AdGroup, db.Model)
    print AdGroup.query.join(AdImage, AdImage.group_id == AdGroup.id).filter().first()
    print AdGroup.query.join(AdImage, AdImage.group_id == AdGroup.id).filter().first()

    print AdGroup,  # vars(AdGroup)
    rdb = AdGroup.use('read_db')
    print rdb.query.filter().first()
    print '------------------'
    print AdGroup.use('write_db').query.filter().first(), AdGroup.use('write_db').query.filter().session.bind
    print vars(AdGroup.use('write_db').query.filter().session)
    print vars(AdGroup.use('read_db').query.filter().session)
    print AdGroup.use('write_db').query.join(AdImage, AdImage.group_id == AdGroup.id).filter().first()


def read3():
    print '---------read_db----------'
    print AdGroup.use('read_db').query.filter().first()  # .to_dict()
    print AdGroup.__bind_key__
    print AdGroup.query.filter().first()
    print AdImage.query.filter().first()
    print '---------write_db----------'
    print AdGroup.use('write_db').query.filter().first()
    print AdGroup.__bind_key__
    print AdGroup.query.filter().first()
    print AdImage.query.filter().first()


def read4():
    print '---------read_db----------'
    print AdGroup.use('read_db').query.join(AdImage, AdImage.group_id == AdGroup.id).first()
    print AdGroup.__bind_key__

    print '---------write_db----------'
    print AdGroup.use('write_db').query.join(AdImage, AdImage.group_id == AdGroup.id).first()
    print AdGroup.__bind_key__


def update():
    print '---------update AdGroup----------'
    a = AdGroup.use('write_db').query.filter().first()
    if not a:
        a = AdGroup()
    a.group_id = 1
    db.session.add(a)
    db.session.commit()


def delete():
    print '---------delete AdGroup----------'
    a = AdGroup.use('write_db').query.filter().first()
    if not a:
        a = AdGroup()
    a.group_id = 1
    db.session.delete(a)
    db.session.commit()


def insert():
    print '---------delete AdGroup----------'
    a = AdGroup.use("write_db")()
    a.name = 'aaaa'
    a.note = 'bbbb'
    db.session.add(a)
    db.session.commit()


if __name__ == "__main__":
    read1()
    # read2()
    # read3()
    read4()
    update()
    delete()
    insert()
