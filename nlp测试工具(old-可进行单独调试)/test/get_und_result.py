# -*- coding: utf-8 -*-

import os
import urllib2
import sys
import json
import time
import xlrd
import yaml
import re
import logging

# 打印日志
logging.debug('This is debug message')
logging.info('This is info message')
logging.warning('This is warning message')
# -------------------------
valid_unit = "ok"
valid_flag = "ok"
valid_name = "ok"
valid_cmd = "ok"
valid_type = "ok"
valid_radio = "ok"
valid_music = "ok"
valid_musician = "ok"
valid_music_cmd = "ok"
valid_music_mode = "ok"
valid_action = "ok"
valid_stock_entity = "ok"
valid_destination_select_strategy = "ok"
valid_domain = "ok"
valid_province = "ok"
valid_city = "ok"
valid_area = "ok"
valid_keyword = "ok"
valid_phone = "ok"
valid_numberInfo = "ok"
valid_key = "ok"
valid_frequency = "ok"
valid_album = "ok"
valid_style = "ok"
valid_storage = "ok"
valid_sMX_datas = "ok"
valid_id = "ok"
valid_adminname = "ok"
valid_time_zone = "ok"
valid_nums = "ok"
valid_phone_name = "ok"
valid_wechat_id = "ok"
valid_wechat_name = "ok"
valid_contactsResults = "ok"
valid_channelId = "ok"
valid_month = "ok"
valid_year = "ok"
valid_day = "ok"
valid_concept = "ok"
valid_data = "ok"
# -------------------------------------------------------------------------------
workfile = 'test/'
host_und = 'http://192.168.128.57:8088/NLPService/parser?userid=AutoTest&key=123'
# 发短信
host_und1 = 'http://192.168.128.57:8088/NLPService/parser?userid=AutoTest&key=123'
# 开机问候语
host_boot = 'http://192.168.128.57:8088/NLPService/welcome?userid=AutoTest&key=123'


# ----------------------------------------获取理解结果(一般)-------------------------------------------
def get_nlpresult(linecontent):
    line_json = json.loads(linecontent)
    # unicode编码转换成 utf-8的编码方式
    text = line_json['text']
    isnew = line_json['isNew']
    # print("----------------------------------------" + type(isnew))
    line_json['isNew'] = int(isnew)
    print line_json['isNew']
    headers = {'Content-Type': 'application/json',
               "Accept-Encoding": "UTF-8",
               "charset": "UTF-8"
               }
    req = ""
    try:
        special = str(sys.argv[5])
        if special == "message":
            req = urllib2.Request(url=host_und1, headers=headers, data=json.dumps(line_json))
        if special == "welcome":
            req = urllib2.Request(url=host_boot, headers=headers, data=json.dumps(line_json))
    except:
        req = urllib2.Request(url=host_und, headers=headers, data=json.dumps(line_json))
    try:
        res_data = urllib2.urlopen(req, timeout=5)
    except Exception as e:
        print e
        print("请求超时")
        return "", text
    # 读取返回结果 res
    res = res_data.read()
    return_result = open("return_result_all.txt", 'a+')
    return_result.write(str(res) + '\n')
    return_result.close()
    return res, text


# ----------------执行对比方法(一般)------------------
def compare_result(text, file_outresult, l, runtime, times):
    # 打开标准文件读取相应字段
    line = l.strip("\n")
    try:
        line_json = json.loads(line)
    except:
        return "json-fail"
    standard_intention = line_json["intention"]
    standard_status = line_json["status"]
    # 打开结果文件
    webcontent_line = open('return_result_short.txt')
    webcontent_line_dict = json.load(webcontent_line)
    webcontent_line_safe = yaml.safe_load_all(line)
    print webcontent_line_dict
    print webcontent_line_safe
    intention = webcontent_line_dict["data"]["intention"]
    status = webcontent_line_dict["data"]["status"]
    answer = webcontent_line_dict["data"]["answer"]
    answer = answer.encode('utf-8')
    print answer
    # 标准字段写入
    file_outresult.write(">>>-------------------------------------------------------------------" + '\n'
                         + "请求服务器时间:" + str(round(runtime, 2)) + "秒" + '\n'
                         + "输入字段:" + text.encode("utf-8") + " (第" + str(times) + "次输入) " + '\n'
                         + "返回结果:{"
                         + "\"intention\":" + "\"" + str(intention) + "\""
                         + "," + "\"status\":" + "\"" + str(status) + "\""
                         )
    # 特殊字段声明全局变量
    global valid_unit, valid_flag, valid_name, valid_cmd, valid_type, valid_radio, valid_music, \
        valid_musician, valid_music_cmd, valid_music_mode, valid_action, valid_stock_entity,\
        valid_destination_select_strategy, valid_domain, valid_province, valid_city, valid_area,\
        valid_keyword, valid_phone, valid_nums,  valid_numberInfo, valid_key, valid_frequency, \
        valid_album, valid_style, valid_storage, valid_sMX_datas, valid_id, valid_adminname, \
        valid_time_zone, valid_wechat_id, valid_wechat_name, valid_phone_name, valid_contactsResults,\
        valid_channelId, valid_month, valid_year, valid_day, valid_concept, valid_data
    # 标准字段判断和写入
    if intention == standard_intention and status == int(standard_status.encode("utf-8")):
        valid_unit = "ok"
    else:
        valid_unit = "fail"
    # 特殊字段判断和写入
    try:
        stock_entity = webcontent_line_dict["data"]["detail"]["stock_entity"]
        standard_stock_entity = line_json["stock_entity"]
        file_outresult.write("\"stock_entity\":" + "\"" + stock_entity.encode("utf-8") + "\"")
        if stock_entity == standard_stock_entity:
            valid_stock_entity = "ok"
        else:
            valid_stock_entity = "fail"
        print("匹配到字段 : stock_entity")
    except Exception as e:
        pass

    try:
        destination_select_strategy = webcontent_line_dict["data"]["detail"]["destination_select_strategy"]
        standard_destination_select_strategy = line_json["destination_select_strategy"]
        file_outresult.write("," + "\"destination_select_strategy\":" +
                             "\"" + destination_select_strategy.encode("utf-8") + "\"")
        if destination_select_strategy == standard_destination_select_strategy:
            valid_destination_select_strategy = "ok"
        else:
            valid_destination_select_strategy = "fail"
        print("匹配到字段 : destination_select_strategy")
    except Exception as e:
        pass

    try:
        music_cmd = webcontent_line_dict["data"]["detail"]["music_cmd"]
        standard_music_cmd = line_json["music_cmd"]
        file_outresult.write("," + "\"music_cmd\":" + "\"" + music_cmd.encode("utf-8") + "\"")
        if music_cmd == standard_music_cmd:
            valid_music_cmd = "ok"
        else:
            valid_music_cmd = "fail"
        print("匹配到字段 : music_cmd")
    except Exception as e:
        pass

    try:
        music_mode = webcontent_line_dict["data"]["detail"]["music_mode"]
        standard_music_mode = line_json["music_mode"]
        file_outresult.write("," + "\"music_mode\":" + "\"" + music_mode.encode("utf-8") + "\"")
        if music_mode == standard_music_mode:
            valid_music_mode = "ok"
        else:
            valid_music_mode = "fail"
        print("匹配到字段 : music_mode")
    except Exception as e:
        pass

    try:
        name = webcontent_line_dict["data"]["detail"]["name"]
        standard_name = line_json["name"]
        file_outresult.write("," + "\"name\":" + "\"" + name.encode("utf-8") + "\"")
        if name == standard_name:
            valid_name = "ok"
        else:
            valid_name = "fail"
        print("匹配到字段 : name")
    except Exception as e:
        pass

    try:
        action = webcontent_line_dict["data"]["detail"]["action"]
        standard_action = line_json["action"]
        file_outresult.write("," + "\"action\":" + "\"" + action.encode("utf-8") + "\"")
        if action == standard_action:
            valid_action = "ok"
        else:
            valid_action = "fail"
        print("匹配到字段 : action")
    except Exception as e:
        pass

    try:
        musician = webcontent_line_dict["data"]["detail"]["musician"]
        standard_musician = line_json["musician"]
        file_outresult.write("," + "\"musician\":" + "\"" + musician.encode("utf-8") + "\"")
        if musician == standard_musician:
            valid_musician = "ok"
        else:
            valid_musician = "fail"
        print("匹配到字段 : musician")
    except Exception as e:
        pass

    try:
        music = webcontent_line_dict["data"]["detail"]["music"]
        standard_music = line_json["music"]
        file_outresult.write("," + "\"music\":" + "\"" + music.encode("utf-8") + "\"")
        if music == standard_music:
            valid_music = "ok"
        else:
            valid_music = "fail"
        print("匹配到字段 : music")
    except Exception as e:
        pass
    try:
        cmd = webcontent_line_dict["data"]["detail"]["cmd"]
        standard_cmd = line_json["cmd"]
        file_outresult.write("," + "\"cmd\":" + "\"" + cmd.encode("utf-8") + "\"")
        if cmd == standard_cmd:
            valid_cmd = "ok"
        else:
            valid_cmd = "fail"
        print("匹配到字段 : cmd")
    except Exception as e:
        pass
    
    try:
        data = webcontent_line_dict["data"]["detail"]["data"]
        standard_data = line_json["data"]
        if data == None or data == "":
            data = "null"
        if standard_data == None:
            standard_data = ""
        if data == None or data == "":
            file_outresult.write("," + "\"data\":null")
        else:
            file_outresult.write("," + "\"data\":" + "\"" + str(data.encode("utf-8")) + "\"")
        if data == standard_data:
            valid_data = "ok"
        else:
            valid_data = "fail"
        print("匹配到字段 : data")
    except Exception as e:
        pass
    
    try:
        flag = webcontent_line_dict["data"]["detail"]["flag"]
        standard_flag = line_json["flag"]
        file_outresult.write("," + "\"flag\":" + "\"" + str(flag) + "\"")
        if flag == int(standard_flag.encode("utf-8")):
            valid_flag = "ok"
        else:
            valid_flag = "fail"
        print("匹配到字段 : flag")
    except Exception as e:
        pass

    try:
        radio = webcontent_line_dict["data"]["detail"]["radio"]
        standard_radio = line_json["radio"]
        file_outresult.write("," + "\"radio\":" + "\"" + str(radio.encode("utf-8")) + "\"")
        if radio == standard_radio:
            valid_radio = "ok"
        else:
            valid_radio = "fail"
        print("匹配到字段 : radio")
    except Exception as e:
        pass


    try:
        domain = webcontent_line_dict["data"]["detail"]["result"]["request"]["domain"]
        standard_domain = line_json["domain"]
        file_outresult.write("," + "\"domain\":" + "\"" + str(domain.encode("utf-8")) + "\"")
        if domain == standard_domain:
            valid_domain = "ok"
        else:
            valid_domain = "fail"
        print("匹配到字段 : domain")
    except Exception as e:
        pass

    try:
        province = webcontent_line_dict["data"]["detail"]["result"]["request"]["params"]["province"]
        standard_province = line_json["province"]
        file_outresult.write("," + "\"province\":" + "\"" + str(province.encode("utf-8")) + "\"")
        if province == standard_province:
            valid_province = "ok"
        else:
            valid_province = "fail"
        print("匹配到字段 : province")
    except Exception as e:
        pass

    try:
        city = webcontent_line_dict["data"]["detail"]["result"]["request"]["params"]["city"]
        standard_city = line_json["city"]
        file_outresult.write("," + "\"city\":" + "\"" + str(city.encode("utf-8")) + "\"")
        if city == standard_city:
            valid_city = "ok"
        else:
            valid_city = "fail"
        print("匹配到字段 : city")
    except Exception as e:
        pass

    try:
        area = webcontent_line_dict["data"]["detail"]["result"]["request"]["params"]["area"]
        standard_area = line_json["area"]
        file_outresult.write("," + "\"area\":" + "\"" + str(area.encode("utf-8")) + "\"")
        if area == standard_area:
            valid_area = "ok"
        else:
            valid_area = "fail"
        print("匹配到字段 : area")
    except Exception as e:
        pass

    try:
        keyword = webcontent_line_dict["data"]["detail"]["result"]["request"]["params"]["keyword"]
        standard_keyword = line_json["keyword"]
        file_outresult.write("," + "\"keyword\":" + "\"" + str(keyword.encode("utf-8")) + "\"")
        if keyword == standard_keyword:
            valid_keyword = "ok"
        else:
            valid_keyword = "fail"
        print("匹配到字段 : keyword")
    except Exception as e:
        pass

    try:
        phone = webcontent_line_dict["data"]["detail"]["phone"]
        standard_phone = line_json["phone"]
        file_outresult.write("," + "\"phone\":" + "\"" + str(phone.encode("utf-8")) + "\"")
        if phone == standard_phone:
            valid_phone = "ok"
        else:
            valid_phone = "fail"
        print("匹配到字段 : phone")
    except Exception as e:
        pass

    try:
        name = webcontent_line_dict["data"]["detail"]["result"]["contactsResults"]["name"]
        standard_name = line_json["name"]
        file_outresult.write("," + "\"name\":" + "\"" + str(name.encode("utf-8")) + "\"")
        if name == standard_name:
            valid_name = "ok"
        else:
            valid_name = "fail"
        print("匹配到字段 : name")
    except Exception as e:
        pass

    try:
        name = webcontent_line_dict["data"]["detail"]["result"]["contactsResults"]["name"]
        standard_name = line_json["name"]
        file_outresult.write("," + "\"name\":" + "\"" + str(name.encode("utf-8")) + "\"")
        if name == standard_name:
            valid_name = "ok"
        else:
            valid_name = "fail"
        print("匹配到字段 : name")
    except Exception as e:
        pass

    try:
        key = webcontent_line_dict["data"]["detail"]["key"]
        standard_key = line_json["key"]
        file_outresult.write("," + "\"key\":" + "\"" + str(key.encode("utf-8")) + "\"")
        if key == standard_key:
            valid_key = "ok"
        else:
            valid_key = "fail"
        print("匹配到字段 : key")
    except Exception as e:
        pass

    try:
        frequency = webcontent_line_dict["data"]["detail"]["frequency"]
        standard_frequency = line_json["frequency"]
        file_outresult.write("," + "\"frequency\":" + "\"" + str(frequency.encode("utf-8")) + "\"")
        if frequency == standard_frequency:
            valid_frequency = "ok"
        else:
            valid_frequency = "fail"
        print("匹配到字段 : frequency")
    except Exception as e:
        pass

    try:
        album = webcontent_line_dict["data"]["detail"]["album"]
        standard_album = line_json["album"]
        file_outresult.write("," + "\"album\":" + "\"" + str(album.encode("utf-8")) + "\"")
        if album == standard_album:
            valid_album = "ok"
        else:
            valid_album = "fail"
        print("匹配到字段 : album")
    except Exception as e:
        pass

    try:
        style = webcontent_line_dict["data"]["detail"]["style"]
        standard_style = line_json["style"]
        file_outresult.write("," + "\"style\":" + "\"" + str(style.encode("utf-8")) + "\"")
        if style == standard_style:
            valid_style = "ok"
        else:
            valid_style = "fail"
        print("匹配到字段 : style")
    except Exception as e:
        pass

    try:
        type = webcontent_line_dict["data"]["detail"]["type"]
        standard_type = line_json["type"]
        file_outresult.write("," + "\"type\":" + "\"" + type.encode("utf-8") + "\"")
        if type == standard_type:
            valid_type = "ok"
        else:
            valid_type = "fail"
        print("匹配到字段 : type")
    except Exception as e:
        pass

    try:
        storage = webcontent_line_dict["data"]["detail"]["storage"]
        standard_storage = line_json["storage"]
        file_outresult.write("," + "\"storage\":" + "\"" + str(storage.encode("utf-8")) + "\"")
        if storage == standard_storage:
            valid_storage = "ok"
        else:
            valid_storage = "fail"
        print("匹配到字段 : storage")
    except Exception as e:
        pass

    try:
        channelId = webcontent_line_dict["data"]["detail"]["data"]["channelId"]
        standard_channelId = line_json["channelId"]
        file_outresult.write("," + "\"channelId\":" + "\"" + str(channelId.encode("utf-8")) + "\"")
        if channelId == standard_channelId:
            valid_channelId = "ok"
        else:
            valid_channelId = "fail"
        print("匹配到字段 : channelId")
    except Exception as e:
        pass

    try:
        adminname = webcontent_line_dict["data"]["detail"]["data"]["weatherList"][0]["location"]["adminname"]
        standard_adminname = line_json["adminname"]
        file_outresult.write("," + "\"adminname\":" + "\"" + str(adminname.encode("utf-8")) + "\"")
        if adminname == standard_adminname:
            valid_adminname = "ok"
        else:
            valid_adminname = "fail"
        print("匹配到字段 : adminname")
    except Exception as e:
        pass

    try:
        time_zone = webcontent_line_dict["data"]["detail"]["data"]["time_zone"]
        standard_time_zone = line_json["time_zone"]
        file_outresult.write("," + "\"time_zone\":" + "\"" + str(time_zone.encode("utf-8")) + "\"")
        if time_zone == standard_time_zone:
            valid_time_zone = "ok"
        else:
            valid_time_zone = "fail"
        print("匹配到字段 : id")
    except Exception as e:
        pass

    try:
        sMX_datas = webcontent_line_dict["data"]["detail"]["result"]["sMX_datas"][0]
        standard_sMX_datas = line_json["sMX_datas"][0]
        file_outresult.write("," + "\"sMX_datas\":" + "\"" + str(sMX_datas.encode("utf-8")) + "\"")
        if sMX_datas == standard_sMX_datas:
            valid_sMX_datas = "ok"
        else:
            valid_sMX_datas = "fail"
        print("匹配到字段 : sMX_datas")
    except:
        try:
            sMX_datas = webcontent_line_dict["data"]["detail"]["result"]["sMX_datas"]
            standard_sMX_datas = line_json["sMX_datas"]
            file_outresult.write("," + "\"sMX_datas\":" + str(sMX_datas))
            if sMX_datas == standard_sMX_datas:
                valid_sMX_datas = "ok"
            else:
                valid_sMX_datas = "fail"
            print("匹配到字段 : sMX_datas")
        except:
            pass
        pass
    # 电话--微信--短信(涉及通讯录) --需要用例进行测试
    try:
        list = webcontent_line_dict["data"]["detail"]["result"]["contactsResults"]
        standard_list = line_json["contactsResults"]
        file_outresult.write("," + "\"contactsResults\":[")
        if "nums" in (list[0]).keys():
            for i in list:
                file_outresult.write("{\"name\":" + str((i["name"]).encode("utf-8")) + ","
                                     + "\"numberInfo\":" + str(i["numberInfo"]) + ","
                                     + "\"nums\":[")
                nums = i["nums"]
                num_len = len(nums)
                b = 1
                for j in (i["nums"]):
                    if b == num_len:
                        file_outresult.write(j.encode("utf-8"))
                    else:
                        file_outresult.write(j.encode("utf-8") + ",")
                    b += 1
                file_outresult.write("]}")
            file_outresult.write("]")
        elif "id" in (list[0]).keys():
            for i in list:
                file_outresult.write("{\"id\":" + str((i["id"]).encode("utf-8")) + ","
                                     + "\"name\":" + str((i["name"]).encode("utf-8")) + "},")
            file_outresult.write("]")
        else:
            file_outresult.write("]")
        try:
            if "nums" in (list[0]).keys():
                for a, b in zip(list, standard_list):
                    # 进来后首先判断name
                    phone_name = a["name"]
                    standard_phone_name = b["name"]
                    if phone_name == standard_phone_name:
                        valid_phone_name = "ok"
                    else:
                        valid_phone_name = "fail"
                        break
                    # 然后判断numberinfo
                    numberInfo = a["numberInfo"]
                    standard_numberInfo = b["numberinfo"]
                    if numberInfo == standard_numberInfo:
                        valid_numberInfo = "ok"
                    else:
                        valid_numberInfo = "fail"
                        break
                    # 然后判断列表中的nums
                    number_list = a["nums"]
                    standard_number_list = b["nums"]
                    for i in range(len(number_list)):
                        if number_list[i] == standard_number_list[i]:
                            valid_nums = "ok"
                        else:
                            valid_nums = "fail"
                            break
                print ("匹配到电话(短信)通讯录字段")
            if "id" in (list[0]).keys():
                for a, b in zip(list, standard_list):
                    # 先判断id
                    wechat_id = a["id"]
                    standard_wechat_id = b["id"]
                    if wechat_id == standard_wechat_id:
                        valid_wechat_id = "ok"
                    else:
                        valid_wechat_id = "fail"
                        break
                    # 然后判断name
                    wechat_name = a["name"]
                    standard_wechat_name = b["name"]
                    if wechat_name == standard_wechat_name:
                        valid_wechat_name = "ok"
                    else:
                        valid_wechat_name = "fail"
                        break
                print ("匹配到微信通讯录")
        except:
            if list == standard_list:
                valid_contactsResults = "ok"
            else:
                valid_contactsResults = "fail"
            print ("匹配到字段 : contactsResults")
    except Exception as e:
        print "special list"
        print e
        pass
    # 天气日期 --无返回结果时 匹配不到adminname字段
    try:
        adminname = webcontent_line_dict["data"]["detail"]["data"]["weatherList"][0]["location"]["adminname"]
        standard_adminname = line_json["adminname"]
        file_outresult.write("," + "\"adminname\":" + "\"" + str(adminname.encode("utf-8")) + "\"")
        if adminname == standard_adminname:
            valid_adminname = "ok"
        else:
            valid_adminname = "fail"
        print("匹配到字段 : adminname")
    except Exception as e:
        pass

    try:
        month = webcontent_line_dict["data"]["detail"]["date"]["month"]
        standard_month = line_json["month"]
        file_outresult.write("," + "\"month\":" + "\"" + str(month.encode("utf-8")) + "\"")
        if month == standard_month:
            valid_month = "ok"
        else:
            valid_month = "fail"
        print("匹配到字段 : month")
    except Exception as e:
        pass

    try:
        year = webcontent_line_dict["data"]["detail"]["date"]["year"]
        standard_year = line_json["year"]
        file_outresult.write("," + "\"year\":" + "\"" + str(year.encode("utf-8")) + "\"")
        if year == standard_year:
            valid_year = "ok"
        else:
            valid_year = "fail"
        print("匹配到字段 : year")
    except Exception as e:
        pass

    try:
        day = webcontent_line_dict["data"]["detail"]["date"]["day"]
        standard_day = line_json["day"]
        file_outresult.write("," + "\"day\":" + "\"" + str(day.encode("utf-8")) + "\"")
        if day == standard_day:
            valid_day = "ok"
        else:
            valid_day = "fail"
        print("匹配到字段 : day")
    except Exception as e:
        pass
    
    try:
        concept = webcontent_line_dict["data"]["detail"]["date"]["concept"]
        standard_concept = line_json["concept"]
        file_outresult.write("," + "\"concept\":" + "\"" + str(concept.encode("utf-8")) + "\"")
        if concept == standard_concept:
            valid_concept = "ok"
        else:
            valid_concept = "fail"
        print("匹配到字段 : concept")
    except Exception as e:
        pass

    # 文件对比结果
    if valid_unit == "ok"\
            and valid_flag == "ok" \
            and valid_name == "ok" \
            and valid_cmd == "ok" \
            and valid_type == "ok" \
            and valid_radio == "ok" \
            and valid_music == "ok" \
            and valid_musician == "ok" \
            and valid_music_cmd == "ok" \
            and valid_music_mode == "ok"\
            and valid_action == "ok" \
            and valid_stock_entity == "ok"\
            and valid_destination_select_strategy == "ok"\
            and valid_domain == "ok"\
            and valid_province == "ok"\
            and valid_city == "ok" \
            and valid_area == "ok"\
            and valid_keyword == "ok"\
            and valid_phone == "ok"\
            and valid_nums == "ok"\
            and valid_numberInfo == "ok" \
            and valid_key == "ok"\
            and valid_frequency == "ok"\
            and valid_album == "ok"\
            and valid_style == "ok"\
            and valid_storage == "ok"\
            and valid_sMX_datas == "ok"\
            and valid_id == "ok"\
            and valid_adminname == "ok"\
            and valid_time_zone == "ok"\
            and valid_wechat_id == "ok"\
            and valid_wechat_name == "ok"\
            and valid_phone_name == "ok" \
            and valid_channelId == "ok"\
            and valid_concept == "ok"\
            and valid_data == "ok":
        file_outresult.write("}"
                             + "\n"
                             + "预期结果:" + line + '\n' + "测试结果:测试成功" + '\n'
                             + "-------------------------------------------------------------------<<<" + '\n\n')
        webcontent_line.close()
        return "--------------------------------测试成功"
    else:
        file_outresult.write("}"
                             + "\n"
                             + "预期结果:" + line + '\n' + "测试结果:测试失败" + '\n'
                             + "-------------------------------------------------------------------<<<" + '\n\n')
        webcontent_line.close()
        # 将错误的返回结果写入到return_result_fail中
        result_fail = open("return_result_fail.txt", "a+")
        return_result_short = open('return_result_short.txt')
        find_res = re.findall(caseid_vue, result_fail.read())
        if find_res:
            pass
        else:
            result_fail.write("<|------------------------" + str(caseid_vue) + "-----------------------|>\n")
        result_fail.write("输入字段为：" + text.encode("utf-8") +  " (第" + str(times) + "次输入) " + "\n")
        result_fail.write(return_result_short.read())
        result_fail.close()
        return_result_short.close()
        return "--------------------------------测试失败"


# ----------------------------------------主执行函数-------------------------------------------
def write_nlp_result():
    # 拿到测试用例()
    test_route = "/opt/test/xiangmu3/TestFrame/testcase/" + table_vue
    test_file = xlrd.open_workbook(test_route)
    sheet = test_file.sheet_by_index(0)
    row_nums = int(caseid_vue.split("_")[1])
    file_in = sheet.cell_value(row_nums, 2)
    file_in = file_in.replace("\n", "")
    file_in = file_in.replace(" ", "")
    file_in = file_in.encode("utf-8")
    file_in = file_in.split("+")
    print file_in
    # 拿到期望文件
    file_exp = sheet.cell_value(row_nums, 6)
    file_exp = file_exp.replace("\n", "")
    file_exp = file_exp.replace(" ", "")
    file_exp = file_exp.encode("utf-8")
    file_exp = file_exp.split("+")
    # 打开返回结果的文件,清空后关闭
    file_output = open('return_result_short.txt', 'w')
    file_output.truncate(0)
    file_output.close()
    # 打开对比结果文件,清空后关闭
    file_outresult = open("compare_result.txt", "w")
    file_outresult.truncate(0)
    file_outresult.close()
    # 打开记录全部返回结果的文件,清空后关闭
    return_result = open("return_result_all.txt", 'w')
    return_result.truncate(0)
    return_result.close()
    # 打开记录错误返回结果文件,清空后返回
    result_fail = open("return_result_fail.txt", "w")
    result_fail.truncate(0)
    result_fail.close()
    l = 1
    for x, y in zip(file_in, file_exp):
        line_json = json.loads(x, encoding="utf-8")
        try:
            text = line_json['text']
        except:
            text = u"text字段不存在"
        # 特殊字段声明全局变量
        global valid_unit, valid_flag, valid_name, valid_cmd, valid_type, valid_radio, valid_music, \
            valid_musician, valid_music_cmd, valid_music_mode, valid_action, valid_stock_entity, \
            valid_destination_select_strategy, valid_domain, valid_province, valid_city, valid_area, \
            valid_keyword, valid_phone, valid_nums, valid_numberInfo, valid_key, valid_frequency, \
            valid_album, valid_style, valid_storage, valid_sMX_datas, valid_id, valid_adminname, \
            valid_time_zone, valid_wechat_id, valid_wechat_name, valid_phone_name, valid_contactsResults,\
            valid_channelId, valid_month, valid_year, valid_day, valid_concept, valid_data
        # 初始化全局变量
        valid_unit = "ok"
        valid_flag = "ok"
        valid_name = "ok"
        valid_cmd = "ok"
        valid_type = "ok"
        valid_radio = "ok"
        valid_music = "ok"
        valid_musician = "ok"
        valid_music_cmd = "ok"
        valid_music_mode = "ok"
        valid_action = "ok"
        valid_stock_entity = "ok"
        valid_destination_select_strategy = "ok"
        valid_domain = "ok"
        valid_province = "ok"
        valid_city = "ok"
        valid_area = "ok"
        valid_keyword = "ok"
        valid_phone = "ok"
        valid_nums = "ok"
        valid_numberInfo = "ok"
        valid_key = "ok"
        valid_frequency = "ok"
        valid_album = "ok"
        valid_style = "ok"
        valid_storage = "ok"
        valid_sMX_datas = "ok"
        valid_id = "ok"
        valid_adminname = "ok"
        valid_time_zone = "ok"
        valid_wechat_id = "ok"
        valid_wechat_name = "ok"
        valid_phone_name = "ok"
        valid_contactsResults = "ok"
        valid_channelId = "ok"
        valid_month = "ok"
        valid_day = "ok"
        valid_year = "ok"
        valid_concept = "ok"
        valid_data = "ok"
        # 打开存放对比结果文件
        file_outresult = open("compare_result.txt", "a+")
        # 请求服务器,获取理解结果
        try:
            s_time = time.time()
            x = x.strip()
            web_content, text = get_nlpresult(x)
            e_time = time.time()
            runtime = e_time - s_time
            print runtime
        except Exception as e:
            print e
            print("请求错误")
            if "请求失败" in y:
                file_outresult.write(">>>---------------------------------------------------------"
                                     + '\n'
                                     + "输入字段:" + text.encode("utf-8") + " (第" + str(l) + "次输入)"
                                     + '\n'
                                     + "返回结果:请求失败(输入字段格式错误或其他原因,请检查后重新请求测试.)"
                                     + '\n'
                                     + "预期结果:" + str(y)
                                     + "\n"
                                     + "测试结果:测试成功"
                                     + '\n'
                                     + "----------------------------------------------------------<<<"
                                     + '\n\n'
                                     )
            else:
                file_outresult.write(">>>---------------------------------------------------------"
                                     + '\n'
                                     + "输入字段:" + text.encode("utf-8") + " (第" + str(l) + "次输入) "
                                     + '\n'
                                     + "返回结果:请求失败(输入字段格式错误或其他原因,请检查后重新请求测试.)"
                                     + '\n'
                                     + "预期结果:" + str(y)
                                     + "\n"
                                     + "测试结果:测试失败"
                                     + '\n'
                                     + "----------------------------------------------------------<<<"
                                     + '\n\n'
                                     )
            file_outresult.close()
            continue
        # 请求超时
        if web_content == "":
            file_outresult.write(">>>---------------------------------------------------------"
                                 + '\n'
                                 + "输入字段:" + text.encode("utf-8") + " (第" + str(l) + "次输入) "
                                 + '\n'
                                 + "返回结果:请求超时,限定请求时间为5秒."
                                 + '\n'
                                 + "预期结果:" + str(y)
                                 + "\n"
                                 + "测试结果:测试失败"
                                 + '\n'
                                 + "----------------------------------------------------------<<<"
                                 + '\n\n'
                                 )
            file_outresult.close()
            continue
        # 拿到返回值,对返回值code进行判断
        web_content_load = json.loads(web_content)
        if web_content_load["code"] == 1:
            print '请求失败,无返回结果'
            file_outresult.write(">>>-----------------------------------------------"
                                 + '\n'
                                 + "输入字段:" + text.encode("utf-8") + " (第" + str(l) + "次输入)"
                                 + '\n'
                                 + "返回结果:云端服务器发生错误,请联系开发人员"
                                 + '\n'
                                 + "预期结果:" + str(y)
                                 + "\n"
                                 + "测试结果:测试失败"
                                 + '\n'
                                 + "------------------------------------------------<<<"
                                 + '\n\n'
                                 )
            file_outresult.close()
            continue

        # 打开存放当前结果文件,清空后写入
        file_output = open('return_result_short.txt', 'w')
        file_output.truncate(0)
        file_output.write(web_content + '\n')
        file_output.close()
        # 调用方法获取对比结果
        result = compare_result(text, file_outresult, y.strip(), runtime, l)
        line_json = json.loads(x)
        text = line_json['text']
        if result == "json-fail":
            if "请求失败" in str(y):
                file_outresult.write(">>>---------------------------------------------------------"
                                     + '\n'
                                     + "输入字段:" + text.encode("utf-8") + " (第" + str(l) + "次输入)"
                                     + '\n'
                                     + "返回结果:云端未按照要求对上述预期结果中的指定字段进行约束(或预期结果格式错误)"
                                     + '\n'
                                     + "预期结果:" + str(y)
                                     + '\n'
                                     + "测试结果:测试成功"
                                     + '\n'
                                     + "----------------------------------------------------------<<<"
                                     + '\n\n'
                                     )
                file_outresult.close()
            else:
                file_outresult.write(">>>---------------------------------------------------------"
                                     + '\n'
                                     + "输入字段:" + text.encode("utf-8") + " (第" + str(l) + "次输入)"
                                     + '\n'
                                     + "返回结果:云端未按照要求对上述预期结果中的指定字段进行约束(或预期结果格式错误)"
                                     + '\n'
                                     + "预期结果:" + str(y)
                                     + '\n'
                                     + "测试结果:测试失败"
                                     + '\n'
                                     + "----------------------------------------------------------<<<"
                                     + '\n\n'
                                     )
                file_outresult.close()

        print result
        l += 1

    print('测试执行完成')

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print ("执行命令如下")
        print ("python get_und_result.py --table 表格名称 --caseid 用例id")
    else:
        # 命令行参数读取
        cue0 = str(sys.argv[0])
        table = str(sys.argv[1])
        table_vue = str(sys.argv[2])
        caseid = str(sys.argv[3])
        caseid_vue = str(sys.argv[4])

        if table == "--table" and caseid == "--caseid":
            print("python" + " " + cue0 + " " + table + " " + table_vue + " " + caseid + " " + caseid_vue)
            start_time = time.time()
            write_nlp_result()
            end_time = time.time()
            runtime = end_time - start_time
            print ("测试运行时间为 : " + str(round(runtime,2)) + "秒")
        else:
            print("命令行参数有误,请重新输入")