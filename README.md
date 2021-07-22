# drift-bottle-in-space

嗨，别来无恙啊，此刻的你是否有些孤独，别怕，此时此刻，在浩瀚宇宙中，总有与你相似的灵魂，你们或许来自不同的星球，有着不同的文明，但你们仍然可以通过太空漂流瓶去表达内心的情感，快来开启你的太空漂流瓶之旅吧......

## 体验

扫描下面二维码，添加机器人为好友（备注信息为**太空漂流瓶**）

![机器人](bot.png)

## 开发指南

1. 申请Wechaty Token [![Powered by Wechaty](https://img.shields.io/badge/Powered%20By-Wechaty-brightgreen.svg)](https://wechaty.js.org) [![Wechaty in Python](https://img.shields.io/badge/Wechaty-Python-blue)](https://github.com/wechaty/python-wechaty)

   具体请访问Wevhaty官网: [https://wechaty.js.org/](https://wechaty.js.org/)

2. 快速上手

   请参考我的文章: [教你用AI Studio+wechaty+阿里云白嫖一个智能微信机器人](https://aistudio.baidu.com/aistudio/projectdetail/1836012)

3. 云服务器

   - 本项目用到了阿里云的云服务器ECS，链接: [云服务器ECS](https://www.aliyun.com/product/ecs)

   - 购买实例后登录[控制台](https://ecs.console.aliyun.com)，实例名称和主机名可以自行更改，记住**公网IP**

   - 有任何不明白的请访问: [云服务器ECS官方文档](https://help.aliyun.com/product/25365.html)

4. 云数据库

   - 本项目用到了阿里云的云数据库RDS MySQL版，链接: [云数据库RDS MySQL版](https://www.aliyun.com/product/rds)

   - 购买实例后登录[控制台](https://rds.console.aliyun.com)，创建一个数据库，名为`drift-bottle-in-space`

   - 创建一个普通账号，授权数据库填写`drift-bottle-in-space`，权限为读写（DDL+DML），记住**用户名**和**密码**

   - 在左侧**数据库连接**处找到外网地址，小本本记下来
   
   - 设置白名单，将云服务器实例的**公网IP**加入白名单

   - 有任何不明白的请访问: [云数据库RDS官方文档](https://help.aliyun.com/product/26090.html)

5. 云存储

   - 本项目用到了阿里云的对象存储OSS，链接: [对象存储OSS](https://www.aliyun.com/product/oss)

   - 开通后登录[控制台](https://oss.console.aliyun.com)，创建一个Bucket，名为`drift-bottle-in-space`

   - 登录[RAM控制台](https://ram.console.aliyun.com)，创建一个用户，访问方式选择**编程访问**，记住`AccessKey ID`和`AccessKey Secret`

   - 有任何不明白的请访问: [云存储OSS官方文档](https://help.aliyun.com/product/31815.html)

6. 克隆本代码仓库

   以任何一种你喜欢❤的方式远程登陆到云服务器

   ```bash
   $ git clone https://github.com/Lovely-Pig/drift-bottle-in-space.git
   ```

7. 安装MySQL客户端

   ```bash
   $ sudo apt install mysql-client-core-8.0
   ```

8. 设置环境变量

   endpoint的设置可参考: [访问域名（Endpoint）](https://help.aliyun.com/document_detail/31837.html?spm=a2c4g.11186623.6.611.554e6d13isyAAt)
   
   ```bash
   $ export HOST="<your host>"    # 云数据库的外网地址
   $ export USER="<your user name>"    # 云数据库账号的用户名
   $ export PASSWORD="<your password>"    # 云数据库账号的密码
   $ export DATABASE="<your database name>"    # 云数据库的数据库名，填写为drift-bottle-in-space
   $ export ACCESS_KEY_ID="<your AccessKey ID>"    # RAM用户的AccessKey ID
   $ export ACCESS_KEY_SECRET="<your AccessKey Secret>"    # RAM用户的AccessKey Secret
   $ export BUCKET_NAME="<your bucket name>"    # 云存储的Bucket，填写为drift-bottle-in-space
   $ export ENDPOINT="<your endpoint>"    # 云存储的访问域名
   ```

9. 运行

   ```bash
   $ cd drift-bottle-in-space
   $ python3 bot.py
   ```

## 参考资料

- [阿里云官网](https://account.aliyun.com)
- [Wechaty官网](https://wechaty.js.org)
- [python-wechaty](https://github.com/wechaty/python-wechaty)
- [python-wechaty-getting-started](https://github.com/wechaty/python-wechaty-getting-started)
- [教你用AI Studio+wechaty+阿里云白嫖一个智能微信机器人](https://aistudio.baidu.com/aistudio/projectdetail/1836012)
