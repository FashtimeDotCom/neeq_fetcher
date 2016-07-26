# -*- coding: utf-8 -*-
import os
import sys
import time


def is_valid_date(date):
    try:
        time.strptime(date, "%Y-%m-%d")
        return True
    except:
        return False


print("备注：常规状态下所有数据将会每日抓取，不需要人工操作\n程序请求输入时输入q可以随时退出（大小写无关）")

while True:
    print("\n这里可以操作的选项有：\n1. 初始化／重置数据库\n2. 抓取指定日期数据\nq. 退出")
    choice = input("请输入（1，2，或者q，大小写无关，输入其他内容无效）: ")
    if choice == "1":
        print("\n－－1. 初始化数据库\n－－备注：初始化／重置表格操作并不会自动重新读取数据")
        sub_choice = input("\n请输入（1，或者q，大小写无关，输入其他内容无效）: ")
        if sub_choice == "1":
            # print("python init_db.py")
            print("初始化／重置交易提示及定期统计（日报）表")
            os.system("python init_db.py")
            print("\n初始化完毕，现在回到最上级菜单\n")
        if sub_choice == "q":
            print("\n再见！\n")
            sys.exit()

    elif choice == "2":
        print("\n需要注意的是，在获取日报统计的时候，一般情况下当天只能获得前一日的数据")
        print(
            "\n－－1. 获取交易提示或定期统计（日报）\n－－2. 获取指定日期范围内的交易提示或定期统计（日报）\n－－3. 获取做市信息（时间较长）\n")
        sub_choice = input("请输入（1，2，3,或者q，大小写无关，输入其他内容无效）: ")
        if sub_choice == "1":
            while True:
                new_choice = input("获取交易提示请输入1，获取定期统计（日报）请输入2：")
                if new_choice == "1":
                    os.system("python tradingtips.py")
                    print("\n获取完毕，现在回到最上级菜单\n")
                    break
                elif new_choice == "2":
                    os.system("python statdata.py")
                    print("\n获取完毕，现在回到最上级菜单\n")
                    break
                elif new_choice.lower() == "q":
                    print("\n再见！\n")
                    sys.exit()
                else:
                    print("\n无意义的指令！\n")
        if sub_choice == "2":
            while True:
                print("\n要求的日期格式： YYYY—MM－DD (例如2016-05-01)")
                start = input("起始日期：")
                end = input("截止日期（需要注意的是，在获取日报统计的时候，一般情况下只能获得一日）：")
                flag = is_valid_date(start) and is_valid_date(end)
                new_choice = input("获取交易提示请输入1，获取定期统计（日报）请输入2：")
                if flag and new_choice == "1":
                    os.system(
                        "python tradingtips.py {} {}".format(start, end))
                    print("\n获取完毕，现在回到最上级菜单\n")
                    break
                elif flag and new_choice == "2":
                    os.system(
                        "python statdata.py {} {}".format(start, end))
                    print("\n获取完毕，现在回到最上级菜单\n")
                    break
                elif new_choice.lower() == "q":
                    print("\n再见！\n")
                    sys.exit()
                else:
                    print("\n无意义的指令！\n")
        if sub_choice == "3":
            print("获取做市信息表")
            os.system("python listedmaker.py")
            print("\n获取做事信息完毕，现在回到最上级菜单\n")
        if sub_choice == "q":
            print("\n再见！\n")
            sys.exit()
    elif choice.lower() == "q":
        print("\n再见！\n")
        sys.exit()
    else:
        print("\n无意义的指令！\n")
