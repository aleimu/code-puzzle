import flask
import flask_sqlalchemy
import flask_restless
from sqlalchemy import Column, ForeignKey, Index, String, SmallInteger, Integer, TIMESTAMP, TEXT, Float, \
    Date, DateTime, TypeDecorator, DECIMAL, BIGINT

# 创建Flask应用和Flask-SQLAlchemy对象
app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://toto:toto123@127.0.0.1:3306/tender?charset=utf8'
db = flask_sqlalchemy.SQLAlchemy(app)


class SpUser(db.Model):
    __tablename__ = 'sp_user'
    # __bind_key__ = 'read_db'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(50))  # 企业名称/合伙人姓名/个人姓名
    user_type = Column(Integer, default=1)  # 合伙人 1 / 个人 2 / 企业 3
    user_no = Column(String(50))  # 企业编号/合伙人工号
    user_phone = Column(String(20))  # 手机号
    org_no = Column(Integer)  # 上级编号
    org_name = Column(String(50))  # 上级名称
    org_type = Column(Integer)  # 上级类型
    legal_name = Column(String(50))  # 法人姓名


# 创建数据库表。
# db.create_all()

# 创建Flask-Restless API管理器
manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)

# 创建API端点，这些端点默认在'/api/<tablename>'可获取。
# 指定允许的HTTP方法也能被这样配置。
manager.create_api(SpUser, methods=['GET', 'POST', 'DELETE'])

if __name__ == '__main__':
    from flask_docs import ApiDoc

    # 需要显示文档的 Api
    app.config['API_DOC_MEMBER'] = ['vx', 'v1', 'api']
    # 需要排除的 RESTful Api 文档
    app.config['RESTFUL_API_DOC_EXCLUDE'] = []
    ApiDoc(app)
    print(vars(app))
    # 启动flask程序
    app.run(host='0.0.0.0', port=3000)
