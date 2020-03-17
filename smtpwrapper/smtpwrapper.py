#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
SMTP wrapper
"""

import smtplib
import time
from email.mime.text import MIMEText

from logni import log


class SMTPwrapper(object):
	""" SMTP wrapper """

	reply_to = None
	user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) '\
		'Gecko/20100101 Thunderbird/60.7.0 Lightning/6.2.7'
	x_mailer = 'smtpwrapper-py'
	content_type = 'plain'
	charset = 'utf-8'

	def __init__(self, smtp='localhost:25'):

		# connect to smtp server
		self.__connect(smtp)


	def __connect(self, smtp):
		""" connect to smtp server """

		try:
			self.connection = smtplib.SMTP(smtp)

		except BaseException as base_err:
			self.connection = None
			log.error('Smtp=%s connect err=%s', (smtp, base_err), priority=2)
			return False

		log.error('Smtp=%s connect ok', (smtp,))
		return True


	def send(self, sender_email, receivers, subject, message, sender_name=None, content_type=None):
		""" simple send mail """

		if not self.connection:
			log.error('Sendmail ERR from=%s, to=%s, err=connect error',\
				(sender_email, receivers,), priority=2)
			return False

		if not sender_email:
			log.error('Sendmail ERR sender must be a input', priority=2)
			return False

		if len(sender_email.split('@')) != 2:
			log.error('Sendmail ERR sender="%s": wrong format', (sender_email,), priority=2)
			return False

		if not receivers:
			log.error('Sendmail ERR receivers must be a input', priority=2)
			return False

		if not subject:
			subject = '(no subject)'

		if not message:
			log.error('Sendmail ERR message must be a input', priority=2)
			return False

		if not content_type:
			content_type = self.content_type

		sender = '%s <%s>' % (sender_email.split('@')[0], sender_email)
		if sender_name:
			sender = '%s <%s>' % (sender_name, sender_email)

		msg = MIMEText(message, content_type, _charset=self.charset)
		msg['Date'] = time.strftime('%a, %d %b %Y %H:%M:%S', time.localtime(time.time()))
		msg['Subject'] = subject
		msg['From'] = sender
		msg['Error-To'] = sender
		msg['Reply-To'] = self.reply_to
		msg['To'] = ', '.join(receivers)
		msg['User-Agent'] = self.user_agent
		msg['X-mailer'] = self.x_mailer

		log.debug('Sendmail message %s', msg)

		return self.__sendmail(sender_email, receivers, msg.as_string())


	def __sendmail(self, sender_email, receivers, msg_string):
		""" smtp send mail """

		try:
			self.connection.sendmail(sender_email, receivers, msg_string)
		except BaseException as base_err:
			log.error('Sendmail ERR from=%s, to=%s, err=%s',\
				(sender_email, receivers, base_err), priority=2)

			return False

		log.error('Sendmail OK from=%s, to=%s, len=%s',\
			(sender_email, receivers, len(msg_string)), priority=2)

		return True


if __name__ == '__main__':

	TS = int(time.time())

	log.mask('ALL')
	log.stderr(1)

	SMTP = SMTPwrapper()
	SMTP.user_agent = 'test agent'
	SMTP.send('erik+test@brozek.name', ['erik@seznam.cz',], 'Test %s' % TS, 'Test email %s' % TS)
