import oss
import time
import mysql
import asyncio
import logging
from typing import Optional, Union

from wechaty_puppet import FileBox, ScanStatus  # type: ignore

from wechaty import Wechaty, Contact
from wechaty.user import Message, Room

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class MyBot(Wechaty):
    """
    listen wechaty event with inherited functions, which is more friendly for
    oop developer
    """
    def __init__(self):
        super().__init__()
        self.hello_msg = '嗨，别来无恙啊，此刻的你是否有些孤独，别怕，此时此刻，在浩瀚宇宙中，总有与你相似的灵魂，你们或许来自不同的星球，有着不同的文明，但你们仍然可以通过太空漂流瓶去表达内心的情感，快来开启你的太空漂流瓶之旅吧......'
        self.bottle_msg = '在六十世纪，地球已不再适合人类生存，人们不得不生活在一个又一个太空飞船里，在宇宙中遨游，而同样遨游的还有各种各样的外星生物，太空漂流瓶是宇宙中交流的唯一途径，它承载着一些情感，在无边的宇宙中漂流，有些漂流瓶很幸运，会被某个有趣的灵魂收到，而有些漂流瓶则可能永远漂流在宇宙中。'
        self.on_bottle_msg_ready = False
        self.on_bottle_img_ready = False
        self.send_bottle_msg = ''
        self.send_bottle_img = ''
        self.get_bottle_msg = ''
        self.get_bottle_img = ''
        self.db = mysql.MySQL(
            host='rm-2zez51ep111kfuz320o.mysql.rds.aliyuncs.com',
            user='lovely_pig',
            password='xu164D1=',
            database='drift-bottle-in-space'
        )
        self.bucket = oss.OSS(
            access_key_id='LTAI5tJ2PUZYmkHNn4eHpneZ',
            access_key_secret='0vGAt1YBjlS2VHFCyu9rFYaA62u758',
            bucket_name='drift-bottle-in-space',
            endpoint='https://oss-cn-beijing.aliyuncs.com',
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
                    conversation = from_contact
                    await conversation.ready()
                    await conversation.say(self.hello_msg)
                    time.sleep(1)
                    await conversation.say('发送太空漂流瓶请回复1，接收太空漂流瓶请回复2。')
                
                if text == '不用了' and self.on_bottle_img_ready:
                    conversation = from_contact
                    self.on_bottle_img_ready = False
                    await conversation.say('好的，正在准备发送太空漂流瓶......')
                    self.db.insert1(
                        table='bottles_dev',
                        fiels='(species, owner, message, image)',
                        values=f'("human", "{conversation.name}", "{self.send_bottle_msg}", "")'
                    )
                    await conversation.say('发送成功🎉🎉🎉')

                if type == Message.Type.MESSAGE_TYPE_IMAGE and self.on_bottle_img_ready:
                    conversation = from_contact
                    self.on_bottle_img_ready = False
                    await conversation.say('好的，正在准备发送太空漂流瓶......')
                    filename = self.db.insert2(
                        table='bottles_dev',
                        fiels='(species, owner, message, image)',
                        values=f'("human", "{conversation.name}", "{self.send_bottle_msg}", "")'
                    )
                    file_box = await msg.to_file_box()
                    await file_box.to_file(file_path=filename)
                    self.bucket.upload_img(filename=filename)
                    await conversation.say('发送成功🎉🎉🎉')

                if self.on_bottle_msg_ready:
                    conversation = from_contact
                    self.on_bottle_msg_ready = False
                    self.on_bottle_img_ready = True
                    self.send_bottle_msg = text
                    await conversation.say('配上一张精美的图片可以更好的表达哦，如不需要请回复不用了。')
                    
                if text == '1':
                    conversation = from_contact
                    self.on_bottle_msg_ready = True
                    await conversation.ready()
                    await conversation.say('请编辑一条您要发送的信息。')

                if text == '2':
                    conversation = from_contact
                    await conversation.ready()
                    await conversation.say('正在尝试接收太空漂流瓶，请稍等.......')
                    bottle_msg, bottle_img = self.db.get_bottle(
                        table='bottles_dev',
                        field='visited, add_time'
                    )
                    time.sleep(1)
                    await conversation.say('接收到一个太空漂流瓶')
                    time.sleep(1)
                    if bottle_msg:
                        await conversation.say(bottle_msg)
                    time.sleep(1)
                    if bottle_img:
                        file_box = FileBox.from_file(path=bottle_img)
                        await conversation.say(file_box)

                if text == '图片':
                    conversation = from_contact

                    # 从网络上加载图片到file_box
                    img_url = 'https://xx.jpg'
                    file_box = FileBox.from_url(img_url, name='xx.jpg')
                    
                    await conversation.ready()
                    await conversation.say('这是自动回复：')
                    await conversation.say(file_box)

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
