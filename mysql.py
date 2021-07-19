import pymysql
import prettytable as pt


class MySQL():
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.wrong_msg = '数据库连接失败😭，请检查连接'
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
        
        except Exception as e:
            self.is_connect = False
            print('数据库连接失败😭')
            print(e)


    def _run(self, table, sql, msg=''):
        # 打开数据库连接
        db = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            charset='utf8'
        )

        _results = []

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
            _results = results[:]
            print('results:', results)

            if results:
                # 打印结果
                tb = pt.PrettyTable()
                tb.field_names = [field for field, value in results[0].items()]
                for i, result in enumerate(results):
                    results[i] = [value for field, value in result.items()]

                tb.add_rows(results)
                if msg:
                    print(msg)
                print(tb.get_string(title=table))

        except Exception as e:
            # 如果发生错误则回滚
            db.rollback()
            print(e)

        finally:
            # 关闭数据库连接
            cursor.close()
            db.close()
        
        return _results


    def table_info(self, table, msg=''):
        if not self.is_connect:
            print(self.wrong_msg)

        else:
            # MySQL语句
            sql = f'''
                DESC {table};
            '''
            if not msg:
                msg = '数据表的信息如下：'

            self._run(table, sql, msg)


    def select_all(self, table, msg=''):
        if not self.is_connect:
            print(self.wrong_msg)
            
        else:
            # MySQL语句
            sql = f'''
                SELECT * FROM {table};
            '''
            if not msg:
                msg = '数据表查询成功😊，全部数据如下：'

            results = self._run(table, sql, msg)

            return results
    

    def get_bottle(self, table, field, msg=''):
        if not self.is_connect:
            print(self.wrong_msg)
            
        else:
            # MySQL语句
            sql = f'''
                SELECT * FROM {table} ORDER BY {field};
            '''
            if not msg:
                msg = '数据表排序成功😊，全部数据如下：'

            # 获取漂流瓶的文本和图片信息
            results = self._run(table, sql, msg)
            message = results[0]['message']
            image = results[0]['image']

            # 修改漂流瓶的访问次数
            id = results[0]['id']
            visited = results[0]['visited']
            self.update(table, content=f'visited={visited + 1}', condition=f'id={id}')

            return message, image
    

    def insert1(self, table, fiels, values, msg=''):
        if not self.is_connect:
            print(self.wrong_msg)
            
        else:
            # MySQL语句
            sql = f'''
                INSERT INTO {table} {fiels} VALUES {values};
            '''
            if not msg:
                msg = '数据插入成功😊，全部数据如下：'

            self._run(table, sql)
            self.select_all(table, msg)


    def insert2(self, table, fiels, values, msg=''):
        if not self.is_connect:
            print(self.wrong_msg)
            
        else:
            # MySQL语句
            sql = f'''
                INSERT INTO {table} {fiels} VALUES {values};
            '''
            if not msg:
                msg = '数据插入成功😊，全部数据如下：'

            self._run(table, sql)
            results = self.select_all(table)
            id = results[-1]['id']
            image = str(id) + '.jpg'
            self.update(table, content=f'image="{image}"', condition=f'id={id}', msg=msg)

            return image
    

    def update(self, table, content, condition, msg=''):
        if not self.is_connect:
            print(self.wrong_msg)
            
        else:
            # MySQL语句
            sql = f'''
                UPDATE {table} SET {content} WHERE {condition};
            '''
            if not msg:
                msg = '数据修改成功😊，全部数据如下：'

            self._run(table, sql)
            self.select_all(table, msg)
    

    def delete(self, table, condition, msg=''):
        if not self.is_connect:
            print(self.wrong_msg)
            
        else:
            # MySQL语句
            sql = f'''
                DELETE FROM {table} WHERE {condition};
            '''
            if not msg:
                msg = '数据删除成功😊，全部数据如下：'

            self._run(table, sql)
            self.select_all(table, msg)


if __name__ == '__main__':
    my_sql = MySQL(
        host='rm-2zez51ep111kfuz320o.mysql.rds.aliyuncs.com',
        user='lovely_pig',
        password='xu164D1=',
        database='drift-bottle-in-space',
    )
    my_sql.table_info(table='test')
    my_sql.select_all(table='test')
    my_sql.insert(table='test', fiels='(test_title, test_date)', values='("测试", NOW())')
    my_sql.update(table='test', content='test_title="学习Python"', condition='test_id=7')
    my_sql.delete(table='test', condition='test_id=8')
