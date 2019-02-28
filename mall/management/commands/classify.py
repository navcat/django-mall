#!/usr/bin/python
#coding=utf-8

"""
初始化商品分类
"""
import re
import json
import logging
from django.db.models import Sum

from django.core.management.base import BaseCommand

from mall.models import Classify


class Command(BaseCommand):
    help = 'Init the classify of products'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--init',
            action='store_true',
            dest='init',
            default=False,
            help='Init the classify of products')

    def handle(self, *args, **options):

        # 保存分类信息
        if options['init']:
            self.stdout.write('init started >>>>>>>>>>>>>')
            return self.deal_init_classify()
        else:
            self.stdout.write('error options >>>>>>>>>>>>>')

    def deal_init_classify(self):
        """ 插入分类信息 """
        parent_list = [
            '酒水食品',
            '家用电器',
            '电脑办公',
            '家具家居',
            '服装服饰',
            '个化护装',
            '衣帽鞋包',
            '运动户外',
            '汽车用品',
            '母婴玩具',
            '医药保健',
            '图书音像',
            '旅游生活'
        ]
        for item in parent_list:
            Classify.objects.get_or_create(name=item)
            self.stdout.write('add classify {0}'.format(item))
