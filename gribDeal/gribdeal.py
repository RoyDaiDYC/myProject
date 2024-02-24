# -*- coding: utf-8 -*-
"""
@Time ： 2024年02月17日   14:02
@Auth ： RoyDai
@File ：gribdeal.py
@IDE ：PyCharm
"""

import pygrib as pg
import pyproj
import numpy

from gribDeal.consoleColor import FontColor
from gribDeal.ntUtils import NTmathUtils


class GribDeal():


    # grib_file_iDegrees是读取的grib文件中横坐标递增变量
    # grib_file_jDegrees是读取的grib文件中纵坐标递增变量
    # zoom是缩放倍数
    def deal_lon_min_max_lat_min_max(self, lon, lat, grib_file_iDegrees, grib_file_jDegrees, zoom):

        global lon_n, lat_n
        lon_n = len(NTmathUtils.get_decimal_part(grib_file_iDegrees))
        lat_n = len(NTmathUtils.get_decimal_part(grib_file_jDegrees))

        hit_lon = NTmathUtils.rounding(lon, lon_n, grib_file_iDegrees)
        hit_lat = NTmathUtils.rounding(lat, lat_n, grib_file_jDegrees)

        i_km = zoom * grib_file_iDegrees
        j_km = zoom * grib_file_jDegrees
        lon_min = NTmathUtils.rounding((hit_lon - grib_file_iDegrees - i_km), lon_n)
        lon_max = NTmathUtils.rounding((hit_lon + grib_file_iDegrees + i_km), lon_n)
        lat_min = NTmathUtils.rounding((hit_lat - grib_file_jDegrees - j_km), lat_n)
        lat_max = NTmathUtils.rounding((hit_lat + grib_file_jDegrees + j_km), lat_n)
        # lonMin=102.6500, lonMax=102.6700, latMin=25.0000, latMax=25.0300
        lonlat_dict = dict({'lon_min': lon_min, 'lon_max': lon_max, 'lat_min': lat_min, 'lat_max': lat_max,
                            'hit_lon': hit_lon, 'hit_lat': hit_lat})

        return lonlat_dict


    def show_grib_data_by_lon_lat(self, file_path, input_lon, input_lat, zoom, places):


        # grib_file = pg.index(file_path, 'name', 'typeOfLevel', 'level')
        grib_file = pg.open(file_path)

        grib_file.seek(0)

        # select = grib_file.select()
        # print(select)

        select_ = grib_file.select()[0]
        file_name = select_.name
        grib_file_iDegrees = select_.iDirectionIncrementInDegrees
        grib_file_jDegrees = select_.jDirectionIncrementInDegrees

        lonLat_minMax = self.deal_lon_min_max_lat_min_max(input_lon, input_lat, grib_file_iDegrees, grib_file_jDegrees,
                                                          zoom)
        hit_lon = lonLat_minMax.get('hit_lon')
        hit_lat = lonLat_minMax.get('hit_lat')

        for _ in grib_file:


            grb = grib_file.select(name=file_name)[grib_file.messagenumber - 1]

            # value = grb.values
            # print(value)
            # 102.6531,25.0078
            grb_name = grb.parameterName
            grb_date = grb.analDate
            grb_forecast_date = grb.validDate

            print(FontColor.set_color(('-' * 50), 'brown', underline=False))
            print('要素名:' + grb_name)
            print('i轴间距' + str(grib_file_iDegrees))
            print('y轴间距' + str(grib_file_jDegrees))
            print(FontColor.set_color('起报时间:', 'brown'),
                  FontColor.set_color(str(grb_date), 'brown'))
            print(FontColor.set_color('预报时间:', 'brown'),
                  FontColor.set_color(str(grb_forecast_date), 'brown'), )
            print(FontColor.set_color(
                '显示' + "[" + FontColor.set_color((str(input_lon) + ',' + str(input_lat)),
                                                   'green') + ']' + FontColor.set_color('坐标最近值', 'red',
                                                                                        underline=False) + '及其' + FontColor.set_color(
                    '周围', 'blue', underline=False) + '格点数据↓', 'brown'))
            print(FontColor.set_color(('-' * 50), 'brown', underline=False))
            value_tuple = grb.data(lat1=lonLat_minMax.get('lat_min'), lat2=lonLat_minMax.get('lat_max'),
                                   lon1=lonLat_minMax.get('lon_min'), lon2=lonLat_minMax.get('lon_max'))
            # print(type(value_tuple))
            # print(value_tuple)


            value_Array_tuple = value_tuple[0]
            value_lat = value_tuple[1]
            value_lon = value_tuple[2]

            # print('value:', type(value))
            # print('value_lat:', type(value_lat))
            # print('value_lon:', type(value_lon))
            # print(end='\t\t')
            print(FontColor.set_color('lon→', 'brown'), end='\t')

            lonArray = value_lon[0]
            lon_hit_index = 0
            for lon_index, lon in enumerate(lonArray):
                lon_v = NTmathUtils.rounding(lon, lon_n)
                if lon_v == hit_lon:
                    lon_hit_index = lon_index
                print(str(lon_v).center(0), end='\t')
            print()
            print(FontColor.set_color('lat↓', 'brown'), end='\t  ')
            # for _ in lonArray:
            #     print('|', end='\t  ' * 2)
            print()
            index = len(value_lat) - 1
            for lat_index, latArray in enumerate(value_lat[::-1]):
                lat_v = NTmathUtils.rounding(latArray[0], lat_n)
                print(str(lat_v).rjust(5), end='\t')
                valueArray = value_Array_tuple[index]
                for value_index, value in enumerate(valueArray):

                    if 'Temperature' == grb_name:
                        value = NTmathUtils.convert_temperature(value=value, input_scale='K', output_scale='C')

                    if lat_v == hit_lat:
                        if value_index == lon_hit_index:
                            print(FontColor.set_color(str(round(value, places)).rjust(5), 'red', underline=True),
                                  end='\t')
                        elif value_index == lon_hit_index - 1:
                            print(FontColor.set_color(str(round(value, places)).rjust(5), 'blue', underline=True),
                                  end='\t')
                        elif value_index == lon_hit_index + 1:
                            print(FontColor.set_color(str(round(value, places)).rjust(5), 'blue', underline=True),
                                  end='\t')
                        else:
                            print(str(NTmathUtils.rounding(value, places)).rjust(5), end='\t')
                    elif lat_v == NTmathUtils.rounding(hit_lat - grib_file_jDegrees, 2):
                        if value_index == lon_hit_index:
                            print(FontColor.set_color(str(round(value, places)).rjust(5), 'blue', underline=True),
                                  end='\t')
                        else:
                            print(str(NTmathUtils.rounding(value, places)).rjust(5), end='\t')
                    elif lat_v == NTmathUtils.rounding(hit_lat + grib_file_jDegrees, 2):
                        if value_index == lon_hit_index:
                            print(FontColor.set_color(str(round(value, places)).rjust(5), 'blue', underline=True),
                                  end='\t')
                        else:
                            print(str(NTmathUtils.rounding(value, places)).rjust(5), end='\t')
                    else:
                        print(str(NTmathUtils.rounding(value, places)).rjust(5), end='\t')
                index -= 1
                print()

        return
