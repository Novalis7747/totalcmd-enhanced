#appModules/totalcmd.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2012 NVDA Contributors
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import appModuleHandler
from NVDAObjects.IAccessible import IAccessible
import speech
import controlTypes
import ui
import scriptHandler

"""
Total Commander enhanced Version 0.91 
Author: Ralf Kefferpuetz and others, June 2018
Features:
- added support for   64bit version of Total Commander
- speaks left/ right for the 2 file windows when moving between them, now also for FTP connections
- added a file index to be spoken in the listView
- added speaking of top and bottom for beginning and end of the listview
- added hotkey Alt-1 to get the current file window announced together with the activated Tab name. If no Tabs are used it announces the current directory instead
- speaks active Tab when control-tab and control-shift-tab is used
"""

currIndex = 0
allIndex = 0
oldActivePannel=0
windowName = ""

class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if self.is64BitProcess:
			if obj.windowClassName in ("LCLListBox", "LCLListBox.UnicodeClass"):
				clsList.insert(0, TCList)
		else:
			if obj.windowClassName in ("TMyListBox", "TMyListBox.UnicodeClass"):
				clsList.insert(0, TCList)


class TCList(IAccessible):

	def event_gainFocus(self):
		global oldActivePannel
		global windowName
		if oldActivePannel !=self.windowControlID:
			oldActivePannel=self.windowControlID
			obj=self
			obj2 = self
			while obj and obj.parent and obj.parent.windowClassName!="TTOTAL_CMD":
				obj=obj.parent
			while obj and obj.previous and obj.windowClassName!="Window":
				obj=obj.previous
			try:
				if obj2.parent.parent.previous.firstChild.role  == 14:
					ui.message(_("left"))
					windowName = "left"
				else:
					ui.message(_("right"))
					windowName = "right"
			except AttributeError:
				pass
		super(TCList,self).event_gainFocus()

	def reportFocus(self):
		if self.name:
			currIndex = self.IAccessibleChildID
			allIndex = self.parent.childCount
			if currIndex == 1: ui.message(_("Top"))
			if allIndex == currIndex: ui.message(_("Bottom"))
			indexString=_("{number} of {total}").format( number = currIndex, total = allIndex)
			speakList=[]
			if controlTypes.STATE_SELECTED in self.states:
				speakList.append(controlTypes.stateLabels[controlTypes.STATE_SELECTED])
			speakList.append(self.name.split("\\")[-1])
			speakList.append(indexString)
			speech.speakMessage(" ".join(speakList))
		else:
			super(TCList,self).reportFocus()

	def script_readActiveTab(self, gesture):
		try:
			obj = self.parent.parent.next.next.firstChild.firstChild.firstChild
			children = obj.children
			for child in children:
				if controlTypes.STATE_SELECTED in child.states:
					infoString = (" %s %s" % (_(windowName), child.name))
					ui.message(infoString)
		except AttributeError:
			pass

		try:
			obj = self.parent.parent.next.next.next.next.firstChild.firstChild.firstChild
			children = obj.children
			for child in children:
				if controlTypes.STATE_SELECTED in child.states:
					infoString = (" %s %s" % (_(windowName), child.name))
					ui.message(infoString)
		except AttributeError:
			pass
		if not children:
			try:
				obj = self.parent.parent.next.next.firstChild
				children = obj.children
				str2 = ":\\"
				for child in children:
					str1 = child.name
					if child.name:
						if str1.find(str2) != -1:
							if windowName == "left":
								infoString = (" %s %s" % (_(windowName), str1))
								ui.message(infoString)
			except AttributeError:
				pass
		
			try:
				obj = self.parent.parent.next.next.next.next.firstChild
				children = obj.children
				str2 = ":\\"
				for child in children:
					str1 = child.name
					if child.name:
						if str1.find(str2) != -1:
							infoString = (" %s %s" % (_(windowName), str1))
							ui.message(infoString)
			except AttributeError:
				pass
	# Translators: Documentation for Alt-1 script.
	script_readActiveTab.__doc__=_("speaks left or right together with the active Tab or working directory.")


	def script_speakActiveTab(self, gesture):
		try:
			gesture.send()
			obj = self.parent.parent.next.next.firstChild.firstChild.firstChild
			children = obj.children
			for child in children:
				if controlTypes.STATE_SELECTED in child.states:
					infoString = child.name
					ui.message(infoString)
					return
		except AttributeError:
			pass

		try:
			obj = self.parent.parent.next.next.next.next.firstChild.firstChild.firstChild
			children = obj.children
			for child in children:
				if controlTypes.STATE_SELECTED in child.states:
					infoString = child.name
					ui.message(infoString)
					return
		except AttributeError:
			pass

	
	__gestures = {
		"kb:alt+1": "readActiveTab",
		"kb:control+tab": "speakActiveTab",
		"kb:control+shift+tab": "speakActiveTab"
	}
