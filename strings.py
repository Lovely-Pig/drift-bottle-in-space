def check(msg):
    msg = msg.replace('\\', '\\\\')
    msg = msg.replace('"', '\\"')
    msg = msg.replace("'", "\\'")
    return msg

if __name__ == '__main__':
    # name = """I'm a pig, o\k"o"""
    # name = 'i"o'
    name = """<img class="emoji emoji1f63c" text="_web" src="/zh_CN/htmledition/v2/images/spacer.gif" />"""
    print(name)
    name = check(name)
    print(name)
