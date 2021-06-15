#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
SMTP wrapper
"""

# pylint: disable=too-few-public-methods
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from logni import log


class SMTPwrapper:
	""" SMTP wrapper """

	reply_to = None
	user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) '\
		'Gecko/20100101 Thunderbird/60.7.0 Lightning/6.2.7'
	x_mailer = 'smtpwrapper-py'
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

		log.info('Smtp=%s connect OK', (smtp,))
		return True


	def send(self, sender_email, receivers, subject, html, txt=None, sender_name=None):
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

		if txt or html:
			pass
		else:
			log.error('Sendmail ERR message must be a input', priority=2)
			return False

		sender = '%s <%s>' % (sender_email.split('@')[0], sender_email)
		if sender_name:
			sender = '%s <%s>' % (sender_name, sender_email)

		msg = MIMEMultipart('alternative')
		msg['Date'] = time.strftime('%a, %d %b %Y %H:%M:%S', time.localtime(time.time()))
		msg['Subject'] = subject
		msg['From'] = sender
		msg['Error-To'] = sender
		msg['Reply-To'] = self.reply_to
		msg['To'] = ', '.join(receivers)
		msg['User-Agent'] = self.user_agent
		msg['X-mailer'] = self.x_mailer

		# Record the MIME types of both parts - text/plain and text/html.
		part_plain = MIMEText(txt, 'plain', _charset=self.charset)
		part_html = MIMEText(html, 'html', _charset=self.charset)

		# Attach parts into message container.
		# According to RFC 2046, the last part of a multipart message, in this case
		# the HTML message, is best and preferred.
		if txt:
			msg.attach(part_plain)
		msg.attach(part_html)

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

		log.info('Sendmail OK from=%s, to=%s, len=%s',\
			(sender_email, receivers, len(msg_string)), priority=2)
		return True


if __name__ == '__main__':

	TS = int(time.time())

	log.mask('ALL')
	log.stderr(1)

	SMTP = SMTPwrapper()
	SMTP.send('erik+test@4.house', ['erik@seznam.cz',], 'Test %s' % TS, '<b>Test email %s</b>' % TS)
