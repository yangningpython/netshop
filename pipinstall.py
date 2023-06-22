# -*- coding: utf-8 -*-
# @DATE : 2021/12/19
# @File : install_package.py
from subprocess import call


def install_package(python_env, pack_path):
    """
    :param python_env: python 环境
    :param pack_path: requirements.txt 的路径
    :return: install failed package
    """
    result = set()
    with open(pack_path, "r") as f:
        packs = f.readlines()
    for pack in packs:
        if not pack:
            continue
        try:
            call("%s -m pip install %s" % (python_env, pack), shell=True)
        except Exception:
            result.add(pack)
    return result
if __name__ == '__main__':
    install_package(r"/root/www/netshop-env/bin/python","requirements.txt")
