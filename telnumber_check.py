#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
     
#正则匹配电话号码
phone="+8613893670000"
p2=re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}')
phonematch=p2.match(phone)
 
if phonematch:
    print phonematch.group()
else:
    print "phone number is error!"
 
#--------www.iplaypython.com---------
 
#正则匹配邮箱和电话号码
emailorphone="aaaaaaaaaa888@sina.cn"
p3=re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}|[^\._-][\w\.-]+@(?:[A-Za-z0-9]+\.)+[A-Za-z]')
emailorphonematch=p3.match(emailorphone)
 
if emailorphone:
    print emailorphonematch.group()
else:
    print "phone or email error..."
