#!/usr/bin/python
# -*- coding: UTF-8 -*-
#程序实现从本地cPickle文件读入联系人名字和对象的键值对字典，实现查询添加列出删除联系人等功能；
#待处理完成再次将字典存入本地文件
import cPickle as p
import sys,time

#定义Person类，包含类变量和类方法
class Person:
	'''定义Person类，包含类变量和类方法.
	
	其中population记录联系人个数，dic_phonebook记录联系人名字和对象的键值对。'''
	population = 0
	dic_phonebook = {}
	
	#对象初始化，完成联系人信息的检查和字典键值对的添加
	def __init__(self, name, phone, stype = 'Other', email = ''):
		'''Initializes the person's data.'''
		self.name = name
		if phone.isdigit() and len(phone) == 11:
			self.phone = phone
		else:
			print 'Error......Wrong phone format!'
			sys.exit()
		self.stype = stype
		if '@' in email and '.' in email:
			self.email = email
		elif email == '':
			self.email = email
		else:
			print 'Error......Wrong email format!'
			sys.exit()
		print '\n......(Initializing %s)......' % self.name
		# When this person is created, he/she
		# adds to the population
		self.__class__.population += 1
		self.__class__.dic_phonebook[name] = self	#将新对象添加到字典，name:Person()
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

	#sayHI
	def sayHi(self):
		'''Greeting by the person.

		Really, that's all it does.'''
		print 'Hi, my name is %s.' % self.name

	#howMany
	def howMany(self):
		'''Prints the current population.'''
		if self.__class__.population == 1:
			print 'I am the only person here.'
		else:
			print 'We have %d persons here.' % self.__class__.population

	#打印联系人信息
	def printinf(self):
		'''Greeting by the person.

		Really, that's all it does.'''
		print 'Hi, my name is %s, my phonenum is %s, my stype is %s' % (self.name,self.phone,self.stype),
		if self.email == '':
			print '.'
		else:
			print ', And my email is %s.' % self.email

def person_search():
	s_name = raw_input('请输入你要搜索的名字：').lower()
	while s_name == '':
		s_name = raw_input('请输入你要搜索的名字：').lower()
	else: 
		if Person.dic_phonebook.has_key(s_name):
			Person.dic_phonebook[s_name].printinf()
		else:
			print '未查询到结果。'
	return 0

def person_new():
	print('请输入你要添加的联系人：')
	s_name = raw_input('name:')
	if Person.dic_phonebook.has_key(s_name):
		print '%s is exsits in your phone_book!' % s_name
		return 0
	s_phone = raw_input('phone:')
	s_stype = raw_input('stype:')
	s_email = raw_input('email:')
	j = raw_input('确定要添加吗？(%s,%s,%s,%s)(y/n)：' % (s_name,s_phone,s_stype,s_email)).lower()
	if j == 'y':
		Person(s_name,s_phone,s_stype,s_email)
	else:
		pass
	return 0

def person_list():
	for s_name in Person.dic_phonebook.keys():
		Person.dic_phonebook[s_name].printinf()
	return 0

def person_delete():	
	print('请输入你要删除的联系人：')
	s_name = raw_input('name:')
	if Person.dic_phonebook.has_key(s_name):
		del Person.dic_phonebook[s_name]
	else:
		print '无此联系人。'
	print '\nPrintDIC......dic_phonebook\'s length is %d.' % len(Person.dic_phonebook)
	return 0

def person_option():
	while True:
		print '*'*50
		print '设置：\n1_清空联系人(C):\n0_退出(Q):\n'	#打印出功能列表
		i = raw_input('请选择操作：').lower()
		if i == '0' or i == 'q':
			break
		elif i == '1' or i == 'c':
			j = raw_input('确实要清空联系人吗？(y/n)：').lower()
			if j == 'y':
				Person.dic_phonebook.clear()
				print '\nPrintDIC......dic_phonebook\'s length is %d.' % len(Person.dic_phonebook)
			else:
				break
		else:
			print 'You have input the wrong character!'	
	return 0

def dic_error():
	print 'You have input the wrong character!'	
	return 0

#主程序，用户不退出时反复循环读取cPickle-->操作联系人-->保存cPickle的流程
dic_func = {'s':person_search,'n':person_new,'l':person_list,'d':person_delete,'o':person_option}
dicpb_file = 'dic_phonebook.data'
# Read back from the storage
with open(dicpb_file) as f:
	Person.dic_phonebook = p.load(f)

#将从文件中读取的字典长度赋值给Person.population
Person.population = len(Person.dic_phonebook)

#处理用户输入，根据不同的输入进行不同的功能操作
i = ''
while i != 'q':
	print
	print '*'*50
	print '1_搜索(s):\n2_新建(n):\n3_列出(l):\n4_删除(d):\n5_设置(o):\n0_退出(q):\n'	#打印出功能列表
	i = raw_input('请选择操作：').lower()
	dic_func.get(i,dic_error)()
	time.sleep(0.5)

# Write to the file
with open(dicpb_file, 'w') as f:
	p.dump(Person.dic_phonebook, f) # dump the object to a file
