import os
import pymysql
import prettytable as pt
from typing import Dict, List, Tuple


class MySQL():
    """
    对数据库进行操作

    用法 ::

        >>> import mysql
        >>> db = mysql.MySQL(
                host='<your host>',
                user='<your user>',
                password='<your password>',
                database='<your database>',
            )
    """
    def __init__(self, host: str, user: str, password: str, database: str):
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


    def _run(self, table: str, sql: str, msg: str = '') -> List[Dict]:
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
        # print('sql:', sql)

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


    def table_info(self, table: str, msg: str = ''):
        """
        查询表的结构
        :param table: 数据表的名称
        :param msg: 运行时打印的提示信息

        用法 ::

            >>> db.table_info(table='bottles_dev')

        """
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


    def select_all(self, table: str, msg: str = '') -> List[Dict]:
        """
        查询表的全部数据
        :param table: 数据表的名称
        :param msg: 运行时打印的提示信息
        :return: 查询的结果

        用法 ::

            >>> db.select_all(table='bottles_dev')

        """
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
    

    def get_bottle(self, table: str, field: str, msg: str = '') -> Tuple[str]:
        """
        获取漂流瓶的信息
        :param table: 数据表的名称
        :param field: 字段名
        :param msg: 运行时打印的提示信息
        :return: 漂流瓶的文本信息, 漂流瓶的图片信息

        用法 ::

            >>> message, image = db.get_bottle(
                    table='bottles_dev',
                    field='visited, add_time'
                )
            >>> print('message:', message)
            >>> print('image:', image)
            message: 这是一条测试信息
            image: 3.jpg

        """
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
    

    def insert1(self, table: str, fields: str, values: str, msg: str = '') -> None:
        """
        发送一个漂流瓶，只有文本信息
        :param table: 数据表的名称
        :param fields: 字段名
        :param values: 值
        :param msg: 运行时打印的提示信息

        用法 ::

            >>> db.insert1(
                    table='bottles_dev',
                    fields='(species, owner, message, image)',
                    values='("human", "九月的海风", "这是另一条测试信息", "")'
                )

        """
        if not self.is_connect:
            print(self.wrong_msg)
            
        else:
            # MySQL语句
            sql = f'''
                INSERT INTO {table} {fields} VALUES {values};
            '''
            if not msg:
                msg = '数据插入成功😊，全部数据如下：'

            self._run(table, sql)
            self.select_all(table, msg)


    def insert2(self, table: str, fields: str, values: str, msg: str = '') -> str:
        """
        发送一个漂流瓶，包含文本信息和图片信息
        :param table: 数据表的名称
        :param fields: 字段名
        :param values: 值
        :param msg: 运行时打印的提示信息
        :return: 图片名

        用法 ::

            >>> db.insert2(
                    table='bottles_dev',
                    fields='(species, owner, message, image)',
                    values='("alien", "细菌", "这是一条测试信息", "")'
                )

        """
        if not self.is_connect:
            print(self.wrong_msg)
            
        else:
            # MySQL语句
            sql = f'''
                INSERT INTO {table} {fields} VALUES {values};
            '''
            if not msg:
                msg = '数据插入成功😊，全部数据如下：'

            self._run(table, sql)
            results = self.select_all(table)
            id = results[-1]['id']
            image = str(id) + '.jpg'
            self.update(table, content=f'image="{image}"', condition=f'id={id}', msg=msg)

            return image
    

    def update(self, table: str, content: str, condition: str, msg: str = '') -> None:
        """
        更改数据的信息
        :param table: 数据表的名称
        :param content: 要更改的内容
        :param condition: 查询的条件
        :param msg: 运行时打印的提示信息

        用法 ::

            >>> db.update(
                    table='bottles_dev',
                    content='visited=1',
                    condition='id=2'
                )

        """
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
    

    def delete(self, table: str, condition: str, msg: str = '') -> None:
        """
        删除数据
        :param table: 数据表的名称
        :param condition: 查询的条件
        :param msg: 运行时打印的提示信息

        用法 ::

            >>> db.delete(
                    table='bottles_dev',
                    condition='id=3'
                )

        """
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
    db = MySQL(
        host=os.getenv('HOST'),
        user=os.getenv('USER'),
        password=os.getenv('PASSWORD'),
        database='drift-bottle-in-space'
    )
    db.table_info(table='bottles_dev')
    db.select_all(table='bottles_dev')
    db.insert1(
        table='bottles_dev',
        fields='(species, owner, message, image)',
        values='("alien", "细菌", "这是一条测试信息", "")'
    )
    db.select_all(table='bottles_dev')
    db.insert1(
        table='bottles_dev',
        fields='(species, owner, message, image)',
        values='("human", "九月的海风", "这是另一条测试信息", "")'
    )
    db.update(
        table='bottles_dev',
        content='visited=1',
        condition='id=2'
    )
    db.delete(
        table='bottles_dev',
        condition='id=1'
    )
