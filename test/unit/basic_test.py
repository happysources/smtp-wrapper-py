#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Unit test
"""

import sys
import time
import unittest

#pylint: disable=wrong-import-position
sys.path.append('../../smtpwrapper/')
sys.path.append('smtpwrapper/')
import smtpwrapper

TS = int(time.time())
PORT = 25
HOSTNAME = 'localhost'
MAIL_FROM_OK = 'erik+test@brozek.name'
MAIL_FROM_ERR = 'email'
MAIL_TO = ['erik@seznam.cz',]
SUBJECT = 'Test %s' % TS
MESSAGE = 'Test email %s' % TS

class TestSmtp(unittest.TestCase):
	""" Unit test """


	def __check_ret_ok(self, ret):
		""" ok response """

		self.assertTrue(ret, msg='return must be value')


	def __check_ret_err(self, ret):
		""" error response """

		self.assertFalse(ret, msg='return must be None')


	def __check_init(self):
		""" check init params """

		self.assertTrue(isinstance(PORT, int), msg='PORT must be integer')



	def test_ok(self):
		"""
		OK test
		"""

		# init
		smtp = smtpwrapper.SMTPwrapper('%s:%s' % (HOSTNAME, PORT))
		self.__check_init()

		ret = smtp.send(MAIL_FROM_OK, MAIL_TO, SUBJECT, MESSAGE)
		self.__check_ret_ok(ret)


	def test_err(self):
		"""
		Error test
		"""

		# init
		smtp = smtpwrapper.SMTPwrapper()
		self.__check_init()

		ret = smtp.send(MAIL_FROM_ERR, MAIL_TO, SUBJECT, MESSAGE)
		self.__check_ret_err(ret)

if __name__ == '__main__':
	unittest.main()
