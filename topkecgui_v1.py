# topKEC GUI, v0.0.1 - Kamil Krawczyk, 2016
# (c) Miller group, Department of Chemistry
# This is a one-way communication device. Will only send messages, not receive error messages.
# TODO Implement a means of receiving communication back from device.

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

		# Connect to the server. 
		# TODO Allow user to select IP address, port number.

		# Server parameters.
		host = '127.0.0.1'
		port = 70

		socketConnect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# Connect to the remote host.
		try:
			socketConnect.connect( (host, port) )

		except:
			self.ErrorOnConnect


		self.InitUI()
		self.Centre()							# Launch application in center.
		self.Show()

	def InitUI(self):

		panel = wx.Panel(self)

		# Text entry labels.
		speedLabel = wx.StaticText(
			panel, 
			-1, 
			"Enter speed (rev/s):"
			)

		speedOption = wx.TextCtrl(
			panel, 
			-1, 
			"1.0", 
			size=(100,-1)
			)

		distanceLabel = wx.StaticText(
			panel, 
			-1, 
			"Enter number of revolutions:"
			)
	
		distanceOption = wx.TextCtrl(
			panel, 
			-1, 
			"1.0", 
			size=(100,-1)
			)

		directionLabel = wx.StaticText(
			panel, 
			-1, 
			"Select direction:"
			)

		# Server response box.
		serverResponse = wx.TextCtrl(
			panel,
			-1,
			"Server response here",
			style=wx.TE_CENTRE,
			size = (300, 50)
			)

		# Title and footer text.
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

		okDistanceButton = wx.Button(
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
		self.Bind

		# GUI setup. Add sizers
		topSizer = wx.BoxSizer(wx.VERTICAL)
		titleSizer = wx.BoxSizer(wx.HORIZONTAL)
		speedSizer = wx.BoxSizer(wx.HORIZONTAL)
		distanceSizer = wx.BoxSizer(wx.HORIZONTAL)
		directionSizer = wx.BoxSizer(wx.HORIZONTAL)
		bottomSizer = wx.BoxSizer(wx.HORIZONTAL)
		responseSizer = wx.BoxSizer(wx.HORIZONTAL)
		infoSizer = wx.BoxSizer(wx.HORIZONTAL)

		# Fill boxes with GUI contents/widgets.
		titleSizer.Add(titleText, 0, wx.ALL, 5)

		speedSizer.Add(speedLabel, 0, wx.ALL, 5)
		speedSizer.Add(speedOption, 0, wx.ALL|wx.EXPAND, 5)
		speedSizer.Add(okSpeedButton, 0, wx.ALL|wx.EXPAND, 5)

		distanceSizer.Add(distanceLabel, 0, wx.ALL, 5)
		distanceSizer.Add(distanceOption, 0, wx.ALL|wx.EXPAND, 5)
		distanceSizer.Add(okDistanceButton, 0, wx.ALL|wx.EXPAND, 5)

		directionSizer.Add(directionLabel, 0, wx.ALL, 5)
		directionSizer.Add(forwardButton, 0, wx.ALL, 5)
		directionSizer.Add(reverseButton, 0, wx.ALL, 5)

		bottomSizer.Add(goButton, 0, wx.ALL, 5)
		bottomSizer.Add(helpButton, 0, wx.ALL, 5)
		bottomSizer.Add(quitButton, 0, wx.ALL, 5)

		responseSizer.Add(serverResponse, 0, wx.ALL|wx.EXPAND, 5)

		infoSizer.Add(footerText, 0, wx.ALL, 5)

		topSizer.Add(titleSizer, 0, wx.CENTER)
		topSizer.Add(wx.StaticLine(panel,), 0, wx.ALL|wx.EXPAND, 5)
		topSizer.Add(speedSizer, 0, wx.ALL|wx.CENTER, 5)
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

	# Other functions.
	def quitProgram(self, event):
		self.Close()

	def closeWindow(self, event):
		self.Destroy()

	def ErrorOnConnect(self, event):
		dial = wx.MessageDialog(
			None, 
			'Cannot connect to server. Restart the software.', 
			'Error', 
			wx.OK|wx.ICON_ERROR
			)
		dial.ShowModal()

if __name__ == '__main__':

	app = wx.App()
	GUIframe(
		None, 
		title="topKEC GUI v0.0.1"					# Set title of window.
		)
	app.MainLoop()
