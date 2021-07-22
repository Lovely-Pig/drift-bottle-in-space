import os
import oss
import time
import mysql
import random
import strings
import asyncio
import logging
from typing import List, Optional, Union

from wechaty_puppet import FileBox, ScanStatus

from wechaty import Wechaty, Contact, Friendship
from wechaty.user import Message, Room

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

SLEEP_TIME = 2

class MyBot(Wechaty):
    """
    listen wechaty event with inherited functions, which is more friendly for
    oop developer
    """
    def __init__(self):
        super().__init__()
        self.hello_msg = '在六十世纪，地球🌏已不再适合人类生存，人们不得不生活在一个又一个太空飞船🚀里，在宇宙中🌌遨游，而同样遨游的还有各种各样的外星生物👽，太空漂流瓶🛸🛸是宇宙中交流的唯一途径，它承载着一些情感，在无边的宇宙中漂流，有些漂流瓶很幸运，会被某个有趣的灵魂收到📡，而有些漂流瓶则可能永远漂流在宇宙中。'
        self.on_bottle_msg_ready = False
        self.on_bottle_img_ready = False
        self.developers: List[Contact] = []
        self.species = 'human'
        self.send_bottle_msg = ''
        # 获取云数据库
        self.db = mysql.MySQL(
            host=os.getenv('HOST'),
            user=os.getenv('USER'),
            password=os.getenv('PASSWORD'),
            database=os.getenv('DATABASE')
        )
        # 创建数据表
        self.db.create_table(table='bottles_dev')
        # 获取云存储
        self.bucket = oss.OSS(
            access_key_id=os.getenv('ACCESS_KEY_ID'),
            access_key_secret=os.getenv('ACCESS_KEY_SECRET'),
            bucket_name=os.getenv('BUCKET_NAME'),
            endpoint=os.getenv('ENDPOINT')
        )


    async def on_message(self, msg: Message):
        """
        listen for message event
        """
        from_contact = msg.talker()
        is_self = msg.is_self()
        text = msg.text()
        type = msg.type()
        room = msg.room()
        
        # 不处理群消息
        if room is None:
            # 不接收机器人自己的消息
            if not is_self:
                if text == 'hi' or text == '你好':
                    await self.say_hello(conversation=from_contact)
                
                # 只发送文本信息
                if text == '不用了' and self.on_bottle_img_ready:
                    await self.send_bottle(
                        conversation=from_contact,
                        msg=msg,
                        on_img=False
                    )

                # 发送文本和图片信息
                if type == Message.Type.MESSAGE_TYPE_IMAGE and self.on_bottle_img_ready:
                    await self.send_bottle(
                        conversation=from_contact,
                        msg=msg,
                        on_img=True
                    )

                # 接收用户编辑的文本信息
                if self.on_bottle_msg_ready:
                    conversation = from_contact
                    self.on_bottle_msg_ready = False
                    self.on_bottle_img_ready = True
                    self.send_bottle_msg = text
                    await conversation.ready()
                    time.sleep(SLEEP_TIME)
                    await conversation.say('配上一张精美的图片🖼🖼️🖼️🖼可以更好的表达此刻的心情哦😉，如不需要请回复不用了。')
                    
                if text == '1':
                    conversation = from_contact
                    self.on_bottle_msg_ready = True
                    await conversation.ready()
                    time.sleep(SLEEP_TIME)
                    await conversation.say('请编辑一条您要发送的信息📝')

                # 伪装外星人发送信息
                if text == '1外星人':
                    conversation = from_contact
                    self.species = 'alien'
                    self.on_bottle_msg_ready = True
                    await conversation.ready()
                    time.sleep(SLEEP_TIME)
                    await conversation.say('您已开启伪装外星人模式，请编辑一条您要发送的信息📝')

                # 接收漂流瓶
                if text == '2':
                    await self.get_bottle(conversation=from_contact)

                # 添加开发者
                if text == '我是开发者':
                    conversation = from_contact
                    await conversation.ready()
                    if from_contact in self.developers:
                        time.sleep(SLEEP_TIME)
                        await conversation.say('您已经是开发者了，无须重复添加哦😉')
                    else:
                        self.developers.append(from_contact)
                        time.sleep(SLEEP_TIME)
                        await conversation.say('您已被添加为开发者，机器人的相关信息会及时向您汇报😁')




    async def say_hello(self, conversation: Contact):
        """
        机器人的自我介绍
        """
        await conversation.ready()
        time.sleep(SLEEP_TIME)
        await conversation.say(self.hello_msg)
        time.sleep(SLEEP_TIME)
        await conversation.say('发送太空漂流瓶请回复1，接收太空漂流瓶请回复2。')


    async def send_bottle(self, conversation: Contact, msg: Message, on_img: bool):
        """
        发送太空漂流瓶
        :param conversation: 用户的contact
        :param msg: 图片的msg
        :param on_img: 是否发送图片

        用法 ::

            >>> # 只发送文本信息
            >>> send_bottle(conversation=from_contact, msg=msg, on_img=False)
            >>> # 发送文本和图片信息
            >>> send_bottle(conversation=from_contact, msg=msg, on_img=True)

        """
        self.on_bottle_img_ready = False
        await conversation.ready()
        time.sleep(SLEEP_TIME)
        await conversation.say('好的，正在准备发送太空漂流瓶🛸......')
        if not on_img:
            self.db.insert1(
                table='bottles_dev',
                fields='(species, owner, message, image)',
                values=f'("{self.species}", "{strings.check(conversation.name)}", "{strings.check(self.send_bottle_msg)}", "")'
            )
        else:
            filename = self.db.insert2(
                table='bottles_dev',
                fields='(species, owner, message, image)',
                values=f'("{self.species}", "{strings.check(conversation.name)}", "{strings.check(self.send_bottle_msg)}", "")'
            )
            file_box = await msg.to_file_box()
            await file_box.to_file(file_path=filename)
            self.bucket.upload_img(dirname='bottles_dev', filename=filename)
            os.remove(path=filename)

        self.species = 'human'
        time.sleep(SLEEP_TIME)
        await conversation.say('发送成功🎉🎉🎉')
        await self.report(msg='有一个用户成功发送了漂流瓶')


    async def get_bottle(self, conversation: Contact):
        """
        接收太空漂流瓶
        :param conversation: 用户的contact

        """
        await conversation.ready()
        time.sleep(SLEEP_TIME)
        await conversation.say('正在尝试接收📡太空漂流瓶🛸，请稍等.......')
        # 50%的概率接收到漂流瓶
        num = random.randint(0, 9)
        if num < 5:
            time.sleep(SLEEP_TIME)
            await conversation.say('十分抱歉😭，飞船附近没有发现漂流瓶🛸')
            await self.report(msg='有一个用户接收漂流瓶失败')
        else:
            bottle_msg, bottle_img = self.db.get_bottle(
                table='bottles_dev',
                field='visited, add_time'
            )
            time.sleep(SLEEP_TIME)
            await conversation.say('接收到一个太空漂流瓶🛸')
            time.sleep(SLEEP_TIME)
            await conversation.say(f'文本消息{"✅" if bottle_msg else "❎"} 图片消息{"✅" if bottle_img else "❎"}')
            if bottle_msg:
                time.sleep(SLEEP_TIME)
                await conversation.say(bottle_msg)
            if bottle_img:
                self.bucket.download_img(dirname='bottles_dev', filename=bottle_img)
                file_box = FileBox.from_file(path=bottle_img)
                time.sleep(SLEEP_TIME)
                await conversation.say(file_box)
                os.remove(path=bottle_img)
            
            await self.report(msg='有一个用户接收漂流瓶成功')
    
    
    async def report(self, msg: str):
        """
        向开发者报告一些信息
        """
        for conversation in self.developers:
            await conversation.ready()
            await conversation.say('尊敬的开发者，您有一条信息📝')
            time.sleep(SLEEP_TIME)
            await conversation.say(msg)
    
    
    async def on_friendship(self, friendship: Friendship):
        if friendship.hello() == '太空漂流瓶':
            await friendship.accept()
            await self.say_hello(conversation=friendship.contact())
            await self.report(msg='新添加一个用户')
    

    async def on_login(self, contact: Contact):
        print(f'user: {contact} has login')


    async def on_scan(self, status: ScanStatus, qr_code: Optional[str] = None,
                      data: Optional[str] = None):
        contact = self.Contact.load(self.contact_id)
        print(f'user <{contact}> scan status: {status.name} , '
              f'qr_code: {qr_code}')


bot: Optional[MyBot] = None


async def main():
    """doc"""
    # pylint: disable=W0603
    global bot
    bot = MyBot()
    await bot.start()


asyncio.run(main())
