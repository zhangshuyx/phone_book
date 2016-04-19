#!/usr/bin/python
# -*- coding: UTF-8 -*-
#程序实现从本地cPickle文件读入联系人名字和对象的键值对字典，实现查询添加列出删除联系人等功能；
#待处理完成再次将字典存入本地文件
#更新vcf导入联系人功能
# ------------------------------------------------------------
# Script   Name: phone_book_vcf.py
# Creation Date: 2016-04-15  10:00
# Last Modified: 2016-04-15  18:00
# Copyright (c)2016, 
# Purpose: This file used for Learning
# ------------------------------------------------------------

 ##############################################
 #   Written by zhangshuyx                    #
 #   zhangshuyx@126.com                       #
 #   http://www.cnblogs.com/zhangshuyx/       #
 ##############################################
import cPickle as p
import sys,time,os.path
from pypinyin import lazy_pinyin as lpy

#定义Person类，包含类变量和类方法
class Person:
	'''定义Person类，包含类变量和类方法.
	
	其中population记录联系人个数，dic_phonebook记录联系人名字和对象的键值对。'''
	population = 0
	dic_phonebook = {}
	
	#对象初始化，完成联系人信息的检查和字典键值对的添加
	def __init__(self, fn, uid, *tels):
		'''Initializes the person's data.'''
		self.fn = fn.decode('utf-8')
		self.uid = uid
		self.tels = tels

		print '\n......(Initializing %s)......' % self.fn
		# When this person is created, he/she
		# adds to the population
		self.__class__.population += 1
		self.__class__.dic_phonebook[''.join(lpy(fn.decode('utf-8')))] = self	#将新对象添加到字典，name:Person()
		print 'Now........ there are %d peoples.' % self.__class__.population

	#对象删除
	def __del__(self):
		'''I am dying.'''
		#print '\n%s says bye.' % self.name

		self.__class__.population -= 1

		#if self.__class__.population == 0:
		#	print 'I am the last one.'
		#else:
		#	print 'There are still %d people left.' % self.__class__.population

	#打印联系人信息
	def printinf(self):
		'''Greeting by the person.

		Really, that's all it does.'''
		print 'Hi, my name is %s, my uid is %s, my tel is %s.' % (self.fn, self.uid, self.tels)
		#for tel in self.tels:
		#	print tel,
		#print self.tels[0],
		#print '.'

#目前的搜索只能根据名字的部分拼音进行搜索，还没实现首字母搜索
def person_search():
	s_name = raw_input('请输入你要搜索的名字的拼音：').lower()
	while s_name == '':
		s_name = raw_input('请输入你要搜索的名字的拼音：').lower()
	else: 
		i = 0
		for key in Person.dic_phonebook.keys():
			if s_name in key:
				Person.dic_phonebook[key].printinf()
				i += 1
		if i == 0:
			print '未查询到结果。'
	return 0

#用户输入的联系人，自动添加全零的uid，若重复给出提示，支持一个联系人多个电话录入
def person_new():
	print('请输入你要添加的联系人(中文）：')
	s_name = raw_input('name:')
	if Person.dic_phonebook.has_key(''.join(lpy(s_name.decode('utf-8')))):
		print '%s is exsits in your phone_book!' % s_name
		return 0
	s_phone = []
	while True:
		s_input = raw_input('phone:')
		if s_input == '': break
		s_phone.append(s_input)
	j = raw_input('确定要添加吗？(%s,%s)(y/n)：' % (s_name,s_phone)).lower()
	if j == 'y':
		Person(s_name,'0000000000000000',s_phone)
	else:
		pass
	return 0

def person_list():
	for s_name in Person.dic_phonebook.keys():
		Person.dic_phonebook[s_name].printinf()
	return 0

def person_delete():	
	print('请输入你要删除的联系人：')
	s_name = ''.join(lpy(raw_input('name:').decode('utf-8')))
	if Person.dic_phonebook.has_key(s_name):
		del Person.dic_phonebook[s_name]
	else:
		print '无此联系人。'
	print '\nPrintDIC......dic_phonebook\'s length is %d.' % len(Person.dic_phonebook)
	return 0

def person_import():	
	vcf_file = raw_input('请输入要导入文件的路径(.vcf)：')
	if not os.path.exists(vcf_file):
		print '文件不存在！'
		return 0
	#i = 0
	fn = uid = ''
	tels = []
	with open(vcf_file) as f:
		for line in f.readlines():
			#if line == 'BEGIN:VCARD\r\n':
				#print 'New person!'
				#pass
			#elif line.startswith('N:'):
			#       lst.append(line[3:-5]+' ')
			if line.startswith('FN:'):
				fn = line[3:-2]
			elif line.startswith('UID:'):
				uid = line[4:-2]
			elif line.startswith('TEL;'):
				tels.append((line[9:-2].split(':')[1]).replace(' ',''))
				#print line[9:-2]+',',
			elif line == 'END:VCARD\r\n':
				Person(fn,uid,tels)
				tels = []
			#i += 1
			#if i >= 24: return 0
	return 0

def person_clear():	
	j = raw_input('确实要清空联系人吗？(y/n)：').lower()
	if j == 'y':
		Person.dic_phonebook.clear()
		print '\nPrintDIC......dic_phonebook cleared! Its length is 0 now.'
	return 0

def person_option():
	while True:
		print '*'*50
		print '设置：\n1.导入联系人(i):\n2.清空联系人(c):\n0.退出(q):\n'	#打印出功能列表
		i = raw_input('请选择操作：').lower()
		if   i == 'q': break
		elif i == 'i': person_import()
		elif i == 'c': person_clear()
		else:
			print 'You have input the wrong character!'	
	return 0

def dic_error():
	print 'You have input the wrong character!'	
	return 0

#主程序，用户不退出时反复循环读取cPickle-->操作联系人-->保存cPickle的流程
if __name__ == "__main__": 
	dic_func = {'s':person_search,'n':person_new,'l':person_list,'d':person_delete,'o':person_option}
	dicpb_file = 'vcf_phonebook.data'
	#第一次执行程序时创建文件并存入示例联系人
	if not os.path.exists(dicpb_file):
		Person('张三','0000000000000000',['12333333333'])
		with open(dicpb_file, 'w') as f:
			p.dump(Person.dic_phonebook, f) # dump the object to a file
		
	# Read back from the storage
	with open(dicpb_file) as f:
		Person.dic_phonebook = p.load(f)

	#将从文件中读取的字典长度赋值给Person.population
	Person.population = len(Person.dic_phonebook)

	#处理用户输入，根据不同的输入进行不同的功能操作
	i = ''
	while True:
		print
		print '*'*50
		print '1.搜索(s):\n2.新建(n):\n3.列出(l):\n4.删除(d):\n5.设置(o):\n0.退出(q):\n'	#打印出功能列表
		i = raw_input('请选择操作：').lower()
		if i == 'q': break
		dic_func.get(i,dic_error)()
		time.sleep(0.5)

	# Write to the file
	with open(dicpb_file, 'w') as f:
		p.dump(Person.dic_phonebook, f) # dump the object to a file
