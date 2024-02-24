# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import pkg_resources

from gribDeal.gribdeal import GribDeal


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print_hi('PyCharm')
    pass
    while True:
        print('请输入文件路径：')
        file_path = input()
        print('输入经纬度逗号隔开：')
        lonlat = input()
        lon = float(lonlat.split(',')[0])
        lat = float(lonlat.split(',')[1])
        print('输入需要放大的倍数：如1倍输入1、2倍输入2')
        zoom = int(input())
        print('输入数值需要保留小数位数：如1位输入1、不保留输入0')
        places = int(input())
        deal = GribDeal()
        deal.show_grib_data_by_lon_lat(file_path, lon, lat, zoom, places)
        print('是否继续输入(y/n*...)：')
        _ = input()
        if _ != 'y':
            break


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
