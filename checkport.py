# coding:utf-8
import paramiko


def getSerList(filename):
    lst = []
    try:
        with open(filename, 'r') as f:
            for line in f.readlines():
                lst.append(line.strip('\r\n'))
    except Exception, e:
        print "file %s error" % filename + str(e)
    finally:
        f.close()
    return lst



def checkPort(webserver, appserver, port):
    flag = True
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    passwd = 'weedfgtt'
    user = 'root'
    while flag:
        try:
            ssh.connect(webserver, 22, user, passwd)
            flag = False
        except Exception, e:
            print str(e)
            print 'Please input %s\'s  %s password: ' % (webserver, user)
            passwd = raw_input()

    stdin, stdout, stderr = ssh.exec_command('telnet %s %s <<! \n^]\n!' % (appserver, port))

    output = stdout.readlines()
    if 'Escape character is' in str(output):
        print '%s\'s port %s is up' % (appserver, port)
    else:
        print '%s\'s port %s is down' % (appserver, port)

    ssh.close()
    return


if __name__ == '__main__':
    webSerList = getSerList('webserver.txt')
    appSerList = getSerList('appserver.txt')
    print 'Please input the port:'
    port = raw_input()
    for web in webSerList:
        for app in appSerList:
            checkPort(web, app, port)
    print webSerList[0]
