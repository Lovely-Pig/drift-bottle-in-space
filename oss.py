import oss2


class OSS():
    def __init__(self, access_key_id, access_key_secret, bucket_name, endpoint):
        # 确认上面的参数都填写正确了
        for param in (access_key_id, access_key_secret, bucket_name, endpoint):
            assert '<' not in param, '请设置参数：' + param

        # 创建Bucket对象，所有Object相关的接口都可以通过Bucket对象来进行
        self.bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)

    def upload_img(self, filename):
        # 上传图片
        key = 'bottles/' + filename
        self.bucket.put_object_from_file(key=key, filename=filename)

    def download_img(self, filename):
        # 下载到本地文件
        key = 'bottles/' + filename
        self.bucket.get_object_to_file(key, filename)

if __name__ == '__main__':
    bucket = OSS(
        access_key_id='LTAI5tJ2PUZYmkHNn4eHpneZ',
        access_key_secret='0vGAt1YBjlS2VHFCyu9rFYaA62u758',
        bucket_name='drift-bottle-in-space',
        endpoint='https://oss-cn-beijing.aliyuncs.com',
    )
    bucket.upload_img(filename='1.jpg')
    bucket.upload_img(filename='2.jpg')
    bucket.upload_img(filename='3.jpg')
    # bucket.download_img(filename='robot.jpg')

