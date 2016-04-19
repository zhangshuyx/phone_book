#!/usr/bin/python
# -*- coding: UTF-8 -*-
# ------------------------------------------------------------
# Script   Name: vcf_parser.py
# Creation Date: 2016-04-15  09:00
# Last Modified: 2016-04-15  11:00
# Copyright (c)2016, 
# Purpose: This file used for Learning
# ------------------------------------------------------------
 
 ##############################################
 #   Written by zhangshuyx                    #
 #   zhangshuyx@126.com                       #
 #   http://www.cnblogs.com/zhangshuyx/       #
 ##############################################

#import os

vcf_file = 'zhangshu.vcf'
i = 0
lst = []
with open(vcf_file) as f:
	for line in f.readlines():
		if line == 'BEGIN:VCARD\r\n':
			#print 'New person!'
			pass
		#elif line.startswith('N:'):
		#	lst.append(line[3:-5]+' ')
		elif line.startswith('FN:'):
			lst.append(line[3:-2]+' ')
		elif line.startswith('UID:'):
			lst.append(line[4:-2]+' [')
		elif line.startswith('TEL;'):
			lst.append((line[9:-2].split(':')[1]+',').replace(' ',''))
			#print line[9:-2]+',',
		elif line == 'END:VCARD\r\n':
			lst.append(']')
			print ''.join(lst)
			lst = []
		i += 1
		if i >= 1000: break
