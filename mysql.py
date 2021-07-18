from typing import Tuple
import pymysql
import prettytable as pt


def run(table, sql):
    # 打开数据库连接
    db = pymysql.connect(
        host='rm-2zez51ep111kfuz320o.mysql.rds.aliyuncs.com',
        user='lovely_pig',
        password='xu164D1=',
        database='drift-bottle-in-space',
        charset='utf8'
    )

    # 创建cursor对象
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)

    try:
        # 执行MySQL语句
        cursor.execute(sql)

        # 获取所有结果
        results = cursor.fetchall()
        print(results)

        # 打印结果
        tb = pt.PrettyTable()
        tb.field_names = [field for field, value in results[0].items()]
        for i, result in enumerate(results):
            results[i] = [value for field, value in result.items()]

        tb.add_rows(results)
        print(tb.get_string(title=table))

        # 提交到数据库执行
        db.commit()

    except:
        # 如果发生错误则回滚
        db.rollback()

    # 关闭数据库连接
    db.close()


def select_all(table):
    # MySQL语句
    sql = f'''
        SELECT * FROM {table};
    '''

    run(table, sql)


def insert(table, fiels: Tuple, values: Tuple):
    # MySQL语句
    sql = f'''
        INSERT INTO {table} {fiels} VALUES {values};
    '''

    run(table, sql)


if __name__ == '__main__':
    select_all(table='test')
    insert(table='test', fiels=(test_title, test_date), values=("测试", NOW()))
