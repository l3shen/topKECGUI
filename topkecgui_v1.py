# topKEC GUI, v0.0.1 - Kamil Krawczyk, 2016
# (c) Miller group, Department of Chemistry
# This is a (sort of) two-way communication device. Will only send messages, not receive error messages.
# I am learning a bit of object-oriented programming and TCP/IP connections in Python.
# This is not going to be an amazing bit of code!
# TODO Implement a loop such that connection is established once and not every time a command is sent.
# TODO Software encoder for the position of the stage.
# TODO Add toggle for rev/s or micron/s.

import wx 
import socket
import select
import string
import sys

class GUIframe(wx.Frame):

	def __init__(self, parent, title):					# Constructor function.
		super(GUIframe, self).__init__(
			parent, 
			title = title, 
			size = (500,500)					# Set size of window.
			)

		self.InitUI()
		self.Centre()							# Launch application in center.
		self.Show()

	def InitUI(self):

		panel = wx.Panel(self)

		# Variables for control. Set to 1 at default.
		speed = 1
		distance = 1

		# Text entry labels.
		speedLabel = wx.StaticText(
			panel, 
			-1, 
			"Enter speed:"
			)

		self.speedOption = wx.TextCtrl(					# MAKE SURE THINGS IN OTHER DEFINITIONS ARE FUCKING LABELLED SELF urggh
			panel, 
			-1, 
			"1.0", 
			size=(100,-1)
			)

		self.distanceOption = wx.TextCtrl(
			panel,
			-1,
			"1.0",
			size = (100,-1)
			)

		# TODO Add distance choice as well.
		distanceLabel = wx.StaticText(
			panel, 
			-1, 
			"Enter distance:"
			)

		directionLabel = wx.StaticText(
			panel, 
			-1, 
			"Select direction:"
			)

		# Options for speed/distance.
		speedOptions = ['rev/s', 'micron/s']
		self.speedChoice = wx.ComboBox(
			panel,
			-1,
			choices = speedOptions,
			style = wx.CB_READONLY
			)

		distanceOptions = ['Revolutions', 'Millimetres']
		self.distanceChoice = wx.ComboBox(
			panel,
			-1,
			choices = distanceOptions,
			style = wx.CB_READONLY
			)

		# Server response box.
		self.serverResponse = wx.TextCtrl(
			panel,
			-1,
			"Server response here",
			style=wx.TE_CENTRE,
			size = (300, 100)
			)

		# Title and footer text/images.
		titleText = wx.StaticText(
			panel,
			-1,
			"Welcome to topKEC."
			)

		footerText = wx.StaticText(
			panel,
			-1,
			"(c) 2016 - Miller Group."
			)
	
		# Control buttons.
		okSpeedButton = wx.Button(
			panel,
			label="OK",
			size = (50,-1)
			)

		forwardButton = wx.Button(
			panel,
			label="Forward",
			size = (100,-1)
			)

		reverseButton = wx.Button(
			panel,
			label="Reverse",
			size = (100,-1)
			)

		quitButton = wx.Button(
			panel, 
			label="Quit topKEC", 
			size=(100,-1)
			)

		goButton = wx.Button(
			panel,
			label="MOVE STAGE",
			size = (100,-1)
			)

		helpButton = wx.Button(
			panel,
			label="HELP",
			size = (100, -1)
			)

		# Event control.
		self.Bind(wx.EVT_BUTTON, self.quitProgram, quitButton)
		self.Bind(wx.EVT_CLOSE, self.closeWindow)
		self.Bind(wx.EVT_BUTTON, self.setSpeed, okSpeedButton)
		self.Bind(wx.EVT_BUTTON, self.setDistanceForward, forwardButton)
		self.Bind(wx.EVT_BUTTON, self.setDistanceReverse, reverseButton)
		self.Bind(wx.EVT_BUTTON, self.moveStage, goButton)
		self.Bind(wx.EVT_BUTTON, self.helpWindow, helpButton)

		# GUI setup. Add sizers
		topSizer = wx.BoxSizer(wx.VERTICAL)
		titleSizer = wx.BoxSizer(wx.HORIZONTAL)
		# logoSizer = wx.BoxSizer(wx.HORIZONTAL)
		speedSizer = wx.BoxSizer(wx.HORIZONTAL)
		distanceSizer = wx.BoxSizer(wx.HORIZONTAL)
		directionSizer = wx.BoxSizer(wx.HORIZONTAL)
		bottomSizer = wx.BoxSizer(wx.HORIZONTAL)
		responseSizer = wx.BoxSizer(wx.HORIZONTAL)
		infoSizer = wx.BoxSizer(wx.HORIZONTAL)

		# Fill boxes with GUI contents/widgets.
		titleSizer.Add(titleText, 0, wx.ALL, 5)

		# logoSizer.Add(logoSplash, 0, wx.ALL, 5)

		speedSizer.Add(speedLabel, 0, wx.ALL, 5)
		speedSizer.Add(self.speedOption, 0, wx.ALL|wx.EXPAND, 5)
		speedSizer.Add(self.speedChoice, 0, wx.ALL|wx.EXPAND, 5)
		speedSizer.Add(okSpeedButton, 0, wx.ALL|wx.EXPAND, 5)

		distanceSizer.Add(distanceLabel, 0, wx.ALL, 5)
		distanceSizer.Add(self.distanceOption, 0, wx.ALL|wx.EXPAND, 5)
		distanceSizer.Add(self.distanceChoice, 0, wx.ALL|wx.EXPAND, 5)

		directionSizer.Add(directionLabel, 0, wx.ALL, 5)
		directionSizer.Add(forwardButton, 0, wx.ALL, 5)
		directionSizer.Add(reverseButton, 0, wx.ALL, 5)

		bottomSizer.Add(goButton, 0, wx.ALL, 5)
		bottomSizer.Add(helpButton, 0, wx.ALL, 5)
		bottomSizer.Add(quitButton, 0, wx.ALL, 5)

		responseSizer.Add(self.serverResponse, 0, wx.ALL|wx.EXPAND, 5)

		infoSizer.Add(footerText, 0, wx.ALL, 5)

		topSizer.Add(titleSizer, 0, wx.CENTER)
		# topSizer.Add(logoSizer, 0, wx.CENTER)
		topSizer.Add(wx.StaticLine(panel,), 0, wx.ALL|wx.EXPAND, 5)
		topSizer.Add(speedSizer, 0, wx.ALL|wx.CENTER, 5)
		topSizer.Add(wx.StaticLine(panel,), 0, wx.ALL|wx.EXPAND, 5)
		topSizer.Add(distanceSizer, 0, wx.ALL|wx.CENTER, 5)
		topSizer.Add(directionSizer, 0, wx.ALL|wx.CENTER, 5)
		topSizer.Add(wx.StaticLine(panel,), 0, wx.ALL|wx.EXPAND, 5)
		topSizer.Add(bottomSizer, 0, wx.ALL|wx.CENTER, 5)
		topSizer.Add(wx.StaticLine(panel,), 0, wx.ALL|wx.EXPAND, 5)
		topSizer.Add(responseSizer, 0, wx.ALL|wx.CENTER, 5)
		topSizer.Add(wx.StaticLine(panel,), 0, wx.ALL|wx.EXPAND, 5)
		topSizer.Add(infoSizer, 0, wx.ALL|wx.CENTER, 5)

		panel.SetSizer(topSizer)
		topSizer.Fit(self)

	# Control and movement functions. Includes connections to socket.
	def setSpeed(self, event):
		# Generate variable from the user response.
		speed = self.speedOption.GetValue()
		command = ''

		# Determine user units of choice.
		speedUnits = self.speedChoice.GetValue()
		if (speedUnits == 'rev/s'):						# If user selects rev/s, it is default.
			command = 'V' + speed + '\n'
		elif (speedUnits == 'micron/s'):
			command = 'V' + str(int(speed * (6.13333e-4))) + '\n'
		
		# TCP/IP communication.
		# TODO Make this a function and not repeat it throughout.
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect(('127.0.0.1', 7777))
		client.send(command)
		resp = client.recv(8192)
		if (len(resp) > 0):
			self.serverResponse.SetValue("Command sent. Velocity set.")
		else:
			self.serverResponse.SetValue("Failed to send command")
		client.shutdown(socket.SHUT_RDWR)
		client.close()

	def moveStage(self, event):
		#TCP/IP communication.
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect(('127.0.0.1', 7777))
		client.send('GO\n')
		resp = client.recv(4096)
		if (len(resp) > 0):
			self.serverResponse.SetValue("Command sent. GO")
		else:
			self.serverResponse.SetValue("Failed to send command")
		client.shutdown(socket.SHUT_RDWR)
		client.close()

	def setDistanceForward(self, event):
		# Generate variable from the user response.
		revForward = float(self.distanceOption.GetValue())
		forwardUnits = self.distanceChoice.GetValue()
		command = ''

		# Determine units of user choice.
		if (forwardUnits == 'Revolutions'):
			command = 'D+' + str(revForward * 25000) + '\n'
		elif (forwardUnits == 'Millimetres'):
			# 1 revolution = 4.91 mm travelled.
			command = 'D+' + str(revForward * (25,000/4.91)) + '\n'

		#TCP/IP communication.
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect(('127.0.0.1', 7777))
		client.send(command)
		resp = client.recv(4096)
		if (len(resp) > 0):
			self.serverResponse.SetValue("Command sent. Distance set forward.")
		else:
			self.serverResponse.SetValue("Failed to send command")
		client.shutdown(socket.SHUT_RDWR)
		client.close()

	def setDistanceReverse(self, event):
		# Generate variable from the user response.
		revReverse = float(self.distanceOption.GetValue())
		reverseUnits = self.distanceChoice.GetValue()
		command = ''
		
		# Determine units of user choice.
		if (reverseUnits == 'Revolutions'):
			command = 'D-' + str(revReverse * 25000) + '\n'
		elif (reverseUnits == 'Millimetres'):
			# 1 revolution = 4.91 mm travelled.
			command = 'D-' + str(revReverse * (25,000/4.91)) + '\n'

		#TCP/IP communication.
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect(('127.0.0.1', 7777))
		client.send(command)
		resp = client.recv(4096)
		if (len(resp) > 0):
			self.serverResponse.SetValue("Command sent. Distance set reverse.")
		else:
			self.serverResponse.SetValue("Failed to send command")
		client.shutdown(socket.SHUT_RDWR)
		client.close()

	# Other functions.
	def quitProgram(self, event):
		self.Close()

	def closeWindow(self, event):
		self.Destroy()

	def helpWindow(self, event):

		description = 	("topKEC is a knife-edge crystallization device designed to create single-crystal "
				"specimens that are ultrathin (order of 100 nm). The device works by fist selecting "
				"a speed, a distance, and a direction, followed by pressing the GO button to initiate "
				"movement. After the movement is complete, you may remove your sample.")

		license = 	("This GUI software is open-source and free to use. It is, in fact, a product of "
				"my own learning in regards to object-oriented program (OOP).")

		info = wx.AboutDialogInfo()

		info.SetIcon(wx.Icon('logo.png', wx.BITMAP_TYPE_PNG))
		info.SetName('topKEC')
		info.SetVersion('0.0.1')
		info.SetDescription(description)
		info.SetCopyright('(C) 2016 Kamil Krawczyk')
		info.SetWebSite('www.kamilkrawczyk.ca')
		info.SetLicence(license)
		info.AddDeveloper('Kamil Krawczyk')

		wx.AboutBox(info)
	
	def speedError(self, event):						# Not really used right now.
		wx.MessageBox(
			'Select a speed unit!', 
			'Error', 
			wx.OK|wx.ICON_ERROR
			)

if __name__ == '__main__':

	app = wx.App()
	GUIframe(
		None, 
		title="topKEC GUI v0.0.1"					# Set title of window.
		)
	app.MainLoop()
