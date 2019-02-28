#!/usr/bin/python
# -*- coding: utf-8 -*-

import locale
from decimal import Decimal
from django import template

register = template.Library()


def accounting(value, place=2):
    """ 用逗号分隔数据 """
    try:
        place = int(place)
    except:
        place = 2

    try:
        value = Decimal(value)
        locale.setlocale(locale.LC_ALL, '')
        return locale.format("%.*f", (place, value), 1)
    except Exception as e:
        print(e)
        return value


register.filter('accounting_format', accounting)