#!/usr/bin/env python
# coding: utf8

# 使用示例
def add_temp_truck(plate, settlement_mode):
    master = db.session.using_bind('master')
    truck = Truck.query.with_session(master).filter_by(plate=plate).update({Truck.settlement_mode: settlement_mode})
    if truck:
        db.session.commit()
        return None, plate
    else:
        return cs.NO_TRUCK, None


"""
这里存放服务需要的一些数据库辅助函数
"""

# 以下代码摘自 https://gist.github.com/adhorn/b84dc47175259992d406
# 用于实现数据库的读写分离
# 同时参考了这里 https://techspot.zzzeek.org/2012/01/11/django-style-database-routers-in-sqlalchemy/

from flask_sqlalchemy import SQLAlchemy, orm, get_state, BaseQuery
from functools import partial
from flask import current_app


class RoutingSession(orm.Session):

    def __init__(self, db, autocommit=False, autoflush=False, **options):
        self.app = db.get_app()
        self.db = db
        self._model_changes = {}
        orm.Session.__init__(
            self, autocommit=autocommit, autoflush=autoflush,
            bind=db.engine,
            query_cls=BaseQuery,
            binds=db.get_binds(self.app), **options)

    def get_bind(self, mapper=None, clause=None):

        try:
            state = get_state(self.app)
        except (AssertionError, AttributeError, TypeError) as err:
            current_app.logger.info(
                "cant get configuration. default bind. Error:" + err)
            return orm.Session.get_bind(self, mapper, clause)

        """
        If there are no binds configured, connect using the default
        SQLALCHEMY_DATABASE_URI
        """
        if state is None or not self.app.config['SQLALCHEMY_BINDS']:
            if not self.app.debug:
                current_app.logger.info("Connecting -> DEFAULT")
            return orm.Session.get_bind(self, mapper, clause)

        elif self._name:
            self.app.logger.debug("Connecting -> {}".format(self._name))
            return state.db.get_engine(self.app, bind=self._name)

        # 有写的情况下必须走主库
        elif self._flushing:  # we who are about to write, salute you
            current_app.logger.info("Connecting -> MASTER")
            return state.db.get_engine(self.app, bind='master')

        else:
            # 默认走主库 除非显式声明要用从库
            # 这样可以避免一些预料不到的逻辑问题
            current_app.logger.info("Connecting -> MASTER")
            return state.db.get_engine(self.app, bind='master')

    _name = None

    def using_bind(self, name):
        s = RoutingSession(self.db)
        vars(s).update(vars(self))
        s._name = name
        return s


class RouteSQLAlchemy(SQLAlchemy):

    def __init__(self, *args, **kwargs):
        SQLAlchemy.__init__(self, *args, **kwargs)
        self.session.using_bind = lambda s: self.session().using_bind(s)

    def create_scoped_session(self, options=None):
        if options is None:
            options = {}
        scopefunc = options.pop('scopefunc', None)
        return orm.scoped_session(
            partial(RoutingSession, self, **options), scopefunc=scopefunc
        )

# db = RouteSQLAlchemy()
