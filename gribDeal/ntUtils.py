# -*- coding: utf-8 -*-
"""
@Time ： 2024年02月17日   14:05
@Auth ： RoyDai
@File ：ntUtils.py
@IDE ：PyCharm
"""


class NTmathUtils():


    def get_decimal_part(num):
        """
        功能：获取小数部分
        参数：
            num: 数字
        """
        if '.' in str(num):
            return str(num).split('.')[1]
        else:
            return ''


    def rounding(num, n=0, degrees=0.0):
        """
        功能：优化Python内置的round()函数有时出现四舍六入的问题，实现真正的四舍五入。
        实现原理：当需要四舍五入的小数点后一位是5时，加1变成6，即可顺利利用round()函数，实现真正的四舍五入。
        参数：
            num: 需要四舍五入的数字；
            n: 保留的小数点位数，默认取整。
            degrees:精确度，如0.01则代表最小精确到0.01，如果是0.05则代表最小精确到0.05
        """
        if float(degrees) != 0.0:
            if num % degrees != degrees:
                if num % degrees > degrees / 2:
                    num = degrees * (num // degrees + 1)
                else:
                    num = degrees * (num // degrees)

        if '.' in str(num):
            if len(str(num).split('.')[1]) > n and str(num).split('.')[1][n] == '5':
                num += 1 * 10 ** -(n + 1)
        if n:
            return round(num, n)
        else:
            return round(num)


    def convert_temperature(value, input_scale, output_scale):
        if input_scale == 'C':
            if output_scale == 'F':
                return value * 1.8 + 32
            elif output_scale == 'K':
                return value + 273.15
            else:
                return value
        elif input_scale == 'F':
            if output_scale == 'C':
                return (value - 32) / 1.8
            elif output_scale == 'K':
                return (value + 459.67) * 5 / 9
            else:
                return value
        elif input_scale == 'K':
            if output_scale == 'C':
                return value - 273.15
            elif output_scale == 'F':
                return value * 9 / 5 - 459.67
            else:
                return value
        else:
            return value


