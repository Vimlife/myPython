# coding:utf-8

import os
import re
import xlsxwriter
import datetime

'''
此脚本用于批量获取主机名的业务IP：
    使用前需在脚本所在目录新建一个hostname.txt文件保存所有主机名,
    每个主机名存一行
    脚本会将获得的业务IP存放在ip.xlsx文件中
'''

hostnames = []
result = {}


def getHostnames(file):
    hostlst = []
    try:
        with open(file, 'r') as f:
            for line in f.readlines():
                hostlst.append(line.strip('\r\n'))
    except Exception, e:
        print 'Open file %s error.' % file
    finally:
        f.close()
    return hostlst


def getIp(hostLst):
    result = {}
    iplist = []
    pattern = re.compile(r'\[(.+)\]')
    for host in hostLst:
        try:
            output = os.popen('ping %s' % host).read()
        except Exception, e:
            print "ping %s occur an error" % host
            print str(e)

        try:
            ip = re.findall(pattern, output)[0]
        except:
            result[host] = 'null'
            print "%s : %s"%(host, ip)
            continue
        result[host] = ip
        print "%s : %s" % (host, ip)
        iplist.append(ip)



    return result,iplist


if __name__ == '__main__':
    hostnames = getHostnames('hostname.txt')
    result,iplist = getIp(hostnames)
    count = len(result)
    ips = ';'.join(iplist)

    print '是否需要生成主机与IP对应的Excel表格？y/n'
    flag = raw_input()

    if flag == 'y':
        t = str(datetime.datetime.now().strftime('%Y%m%d%H%M'))
        workbook = xlsxwriter.Workbook('ip%s.xlsx' % t)
        worksheet = workbook.add_worksheet('sheet1')
        worksheet.set_column('A:A', 30)
        worksheet.set_column('B:B', 30)
        worksheet.write(0, 0, 'hostname')
        worksheet.write(0, 1, 'ip')
        i = 1
        keys = result.keys()
        hosts = sorted(keys)
        for key in hosts:
            if i <= count:
                worksheet.write(i, 0, key)
                worksheet.write(i, 1, str(result[key]))
            i = i + 1
        worksheet.write(0,2,ips)
        workbook.close()


    # print result
    print ips
