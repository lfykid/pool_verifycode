# -*- coding: utf-8 -*-
# !/usr/bin/env python


import os
from Util.utilClass import ConfigParse
from Util.utilClass import LazyProperty


class GetConfig(object):
    """
    to get config from config.ini
    """

    def __init__(self):
        self.pwd = os.path.split(os.path.realpath(__file__))[0]
        self.config_path = os.path.join(os.path.split(self.pwd)[0], 'Config.ini')
        self.config_file = ConfigParse()
        self.config_file.read(self.config_path)


    @LazyProperty
    def proxy_getter_functions(self):
        return self.config_file.options('ProxyGetter')

    @LazyProperty
    def host_ip(self):
        return self.config_file.get('HOST','ip')

    @LazyProperty
    def host_port(self):
        return int(self.config_file.get('HOST', 'port'))

    @LazyProperty
    def mysql_url(self):
        return self.config_file.get('DB', 'MYSQL_URL')


if __name__ == '__main__':
    gg = GetConfig()
    print(gg.proxy_getter_functions)
    print(gg.host_ip)
    print(gg.host_port)
