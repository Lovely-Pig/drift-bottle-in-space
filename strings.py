def check(msg: str) -> str:
    """
    对字符串中的特殊字符加上转义字符`/`
    :param msg: 输入字符串
    :return: 加上转义字符后的字符串

    用法 ::

        >>> import strings
        >>> msg = strings.check(msg="I'm a lovely pig.")
        >>> print(msg)
        I\\'m a lovely pig.

    """
    msg = msg.replace('\\', '\\\\')
    msg = msg.replace('"', '\\"')
    msg = msg.replace("'", "\\'")

    return msg


if __name__ == '__main__':
    name = "I'm a lovely pig."
    print(name)
    name = check(name)
    print(name)
