import pymysql
import prettytable as pt

def select_all(table='test'):
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

    sql = f'''
        SELECT * FROM {table};
    '''

    try:
        # 执行MySQL语句
        cursor.execute(sql)

        # 获取所有结果
        results = cursor.fetchall()
        print(results)

        # 打印结果
        tb = pt.PrettyTable()
        # tb.field_names = ['id', 'name']
        table.add_rows(results)
        print(tb)

        # 提交到数据库执行
        db.commit()

    except:
        # 如果发生错误则回滚
        db.rollback()

    # 关闭数据库连接
    db.close()

if __name__ == '__main__':
    select_all()
