#!/usr/bin/python
# -*- coding: UTF-8 -*-
#程序实现从本地cPickle文件读入联系人名字和对象的键值对字典，实现查询添加列出删除联系人等功能；
#待处理完成再次将字典存入本地文件
#更新vcf导入联系人功能
# ------------------------------------------------------------
# Script   Name: phone_book_vcf.py
# Creation Date: 2016-04-15  10:00
# Last Modified: 2016-04-20  09:50
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
try:
	from pypinyin import lazy_pinyin as lpy
except:
	print('Error......You must install the pypinyin module first!')
	sys.exit()

#定义Person类，包含类变量和类方法
class Person:
	'''定义Person类，包含类变量和类方法.
	
	其中population记录联系人个数，dic_phonebook记录联系人名字和对象的键值对。'''
	population = 0
	dic_phonebook = {}
	
	#对象初始化，完成联系人信息的检查和字典键值对的添加
	def __init__(self, fn, uid, tels):
		'''Initializes the contact's data.'''
		self.fn = fn.decode('utf-8')
		self.uid = uid
		self.tels = tels

		print '\n......(Initializing %s)......' % self.fn
		# When this contact is created, he/she
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
		'''Greeting by the contact.

		Really, that's all it does.'''
		print 'Hi, my name is %s, my uid is %s, my tel is %s.' % (self.fn, self.uid, ','.join(self.tels))

	#导出联系人信息
	def exportinf(self):
		'''Greeting by the contact.

		Really, that's all it does.'''
		return '%s,%s,%s' % (self.fn, self.uid, ','.join(self.tels))

#目前的搜索只能根据名字的部分拼音进行搜索，还没实现首字母搜索
def contact_search():
	s_name = ''.join(lpy(raw_input('请输入你要搜索的名字部分(Please input the search string):').decode('utf-8')))
	while s_name == '':
		s_name = ''.join(lpy(raw_input('请输入你要搜索的名字部分(Please input the search string):').decode('utf-8')))
	else: 
		i = 0
		for key in Person.dic_phonebook.keys():
			if s_name in key:
				Person.dic_phonebook[key].printinf()
				i += 1
		if i == 0:
			print '未查询到结果。(No result found.)'
		else:
			print '共查询到%d条记录。(%d results found.)' % (i,i)
	return 0

#用户输入的联系人，自动添加全零的uid，若重复给出提示，支持一个联系人多个电话录入
def contact_new():
	print('请输入你要添加的联系人(中文）(Please input the name)：')
	s_name = raw_input('name:')
	if Person.dic_phonebook.has_key(''.join(lpy(s_name.decode('utf-8')))):
		print '%s is exsits in your phone_book!' % s_name
		return 0
	s_phone = []
	while True:
		s_input = raw_input('phone:')
		if s_input == '':
			break
		elif not s_input.replace(' ','').replace('+','').isdigit():
			print ('Error......telnum format error! Please retry.')
			continue
		s_phone.append(s_input)
	j = raw_input('确定要添加吗？(Are you sure?)(%s,%s)(y/n)：' % (s_name,s_phone)).lower()
	if j == 'y':
		Person(s_name,'0000000000000000',s_phone)
	else:
		pass
	return 0

def contact_list():
	for s_name in Person.dic_phonebook.keys():
		Person.dic_phonebook[s_name].printinf()
	return 0

def contact_delete():	
	print('请输入你要删除的联系人：(The name to be deleted:)')
	s_name = ''.join(lpy(raw_input('name:').decode('utf-8')))
	if Person.dic_phonebook.has_key(s_name):
		del Person.dic_phonebook[s_name]
		print('Success......%s has been deleted!' % s_name)
	else:
		print 'Error......无此联系人。(Found none.)'
	print '\nPrintDIC......dic_phonebook\'s length is %d.' % len(Person.dic_phonebook)
	return 0

def contact_import():	
	vcf_file = raw_input('请输入要导入文件的路径(File to be imported:)(.vcf)：')
	if not os.path.exists(vcf_file):
		print '文件不存在！(File not found!)'
		return 0
	#i = 0
	fn = uid = ''
	tels = []
	with open(vcf_file) as f:
		for line in f.readlines():
			#if line == 'BEGIN:VCARD\r\n':
				#print 'New contact!'
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

def contact_export():
	lst = []
	export_file = 'export.csv'
	try:
		with open(export_file,'w') as f:
			for p in Person.dic_phonebook.values():
				lst.append(p.exportinf())
			f.write('\n'.join(lst).encode('utf-8'))
		print 'Exporting......to %s success. ' % export_file
	except:
		print 'Exporting......error, please check the program!'
def contact_clear():	
	j = raw_input('确实要清空联系人吗？(Are you sure?)(y/n)：').lower()
	if j == 'y':
		Person.dic_phonebook.clear()
		print '\nPrintDIC......dic_phonebook cleared! Its length is 0 now.'
	return 0

def contact_option():
	option_func = {'i':contact_import,'e':contact_export,'c':contact_clear}
	while True:
		print '*'*50
		print '>>>设置/Option(o):\n\t>>>导入联系人/Import_contacts_vcf(i):\n\t>>>导出联系人/Export_contacts_csv(e):\n\t>>>清空联系人/Clear_contacts(c):\n\t>>>退出/Quit(q):\n'	#打印出功能列表
		i = raw_input('请选择操作(Please select:)：').lower()
		if i == 'q': break
		option_func.get(i,dic_error)()
		time.sleep(0.5)
	return 0

def dic_error():
	print 'You have input the wrong character!'	
	return 0

#主程序，首先检查是否存在data文件，不存在则创建并写入示例
#用户不退出时反复循环读取用户输入并执行相应操作，最后保存cPickle
if __name__ == "__main__": 
	dic_func = {'s':contact_search,'n':contact_new,'l':contact_list,'d':contact_delete,'o':contact_option}
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
		print '当前联系人总数(Totle contacts now):%d.\n\n>>>搜索/Search(s):\n>>>新建/New(n):\n>>>列出/List(l):\n>>>删除/Delete(d):\n>>>设置/Option(o):\n>>>退出/Quit(q):\n' % len(Person.dic_phonebook)	#打印出功能列表
		i = raw_input('请选择操作(Please select)：').lower()
		if i == 'q': break
		dic_func.get(i,dic_error)()
		time.sleep(0.5)

	# Write to the file
	with open(dicpb_file, 'w') as f:
		p.dump(Person.dic_phonebook, f) # dump the object to a file
