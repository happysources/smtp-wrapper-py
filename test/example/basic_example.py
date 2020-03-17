#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Example for MySQL wrapper
"""

import sys
import time
sys.path.append('smtpwrapper')

import smtpwrapper

TS = int(time.time())
SMTP = smtpwrapper.SMTPwrapper()
SMTP.user_agent = 'test agent'
print(SMTP.send('erik+test@brozek.name', ['erik@seznam.cz',], 'Test %s' % TS, 'Test email %s' % TS))
