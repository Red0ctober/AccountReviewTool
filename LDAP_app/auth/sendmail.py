import smtplib

class SendMessage():

	def __init__(self, sender):
		self.s = sender
		receivers = ['ogiramma@ssc.wisc.edu']
	
		message = """From: Consult <consult@ssc.wisc.edu>
To: Oliver <ogiramma@ssc.wisc.edu>
Subject: Test Email

This is a test message."""
	
		try:
			smtpObj = smtplib.SMTP('localhost')
			smtpObj.sendmail(self.s, receivers, message)
			print('Email Sent')
		
		except:
			print ("Error: unable to send")	