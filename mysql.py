import pymysql


# 打开数据库连接
db = pymysql.connect(
    host='rm-2zez51ep111kfuz320o.mysql.rds.aliyuncs.com',
    user='lovely_pig',
    password='xu164D1=',
    database='drift-bottle-in-space',
    charset='utf8'
)

# 创建cursor对象
cursor = db.cursor()

sql = '''
    DESC test;
'''

try:
    # 执行MySQL语句
    cursor.execute(sql)

    data = cursor.fetchone()
    print(data)

    # 提交到数据库执行
    db.commit()

except:
    # 如果发生错误则回滚
    db.rollback()

# 关闭数据库连接
db.close()
