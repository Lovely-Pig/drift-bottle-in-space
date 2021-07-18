import pymysql
import prettytable as pt


class MySQL():
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        try:
            # 检查数据库连接是否成功
            db = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                charset='utf8'
            )
            db.close()
            self.is_connect = True
            print('数据库连接成功😊')
        
        except:
            self.is_connect = False
            print('数据库连接失败😭')


    def _run(self, table, sql):
        # 打开数据库连接
        db = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            charset='utf8'
        )

        # 创建cursor对象
        cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
        print('sql:', sql)

        try:
            # 执行MySQL语句
            cursor.execute(sql)

            # 提交到数据库执行
            db.commit()

            # 获取所有结果
            results = cursor.fetchall()
            print('results:', results)

            # 打印结果
            tb = pt.PrettyTable()
            tb.field_names = [field for field, value in results[0].items()]
            for i, result in enumerate(results):
                results[i] = [value for field, value in result.items()]

            tb.add_rows(results)
            print(tb.get_string(title=table))

        except:
            # 如果发生错误则回滚
            db.rollback()

        # 关闭数据库连接
        cursor.close()
        db.close()


    def table_info(self, table):
        # MySQL语句
        sql = f'''
            DESC {table};
        '''

        self._run(table, sql)


    def select_all(self, table):
        # MySQL语句
        sql = f'''
            SELECT * FROM {table};
        '''

        self._run(table, sql)


    def insert(self, table, fiels, values):
        # MySQL语句
        sql = f'''
            INSERT INTO {table} {fiels} VALUES {values};
        '''

        self._run(table, sql)
        self.select_all(table)


if __name__ == '__main__':
    host='rm-2zez51ep111kfuz320o.mysql.rds.aliyuncs.com'
    user='lovely_pig'
    password='xu164D1='
    database='drift-bottle-in-space'
    my_sql = MySQL(host, user, password, database)
    my_sql.table_info(table='test')
    my_sql.select_all(table='test')
    my_sql.insert(table='test', fiels='(test_title, test_date)', values='("测试", NOW())')
