import sublime, sublime_plugin

class PromptGotoLoCoCommand(sublime_plugin.WindowCommand):

	def run(self):
		self.window.show_input_panel("Goto line:col", "", self.on_done, None, None)
		pass

	def on_done(self, text):		
		try:
			line, col = self.parseLineCol(text)
			if self.window.active_view():
				self.window.active_view().run_command("goto_lo_co", {"line": line, "col": col})
		except ValueError:
			pass
	
	# Parses user input into seperate line and column variables
	def parseLineCol(self, text):
		lineNum = ""
		colNum = ""

		delimiter = [':', ',', ' ', '\t', ';']
		foundDelim = 0
		skipDelim = 0
		
		for ch in text:
			for d in delimiter:
				if ch == d:
					foundDelim = 1
					skipDelim = 1

			if foundDelim == 0:
				lineNum += ch
			else:
				# Skip the recording of the delimiter
				if skipDelim == 1:
					skipDelim = 0
				else:
					colNum += ch

		# If found no delimiter, go to first column
		if foundDelim == 0:
			colNum += str(1)

		return (lineNum, colNum)

class GotoLoCoCommand(sublime_plugin.TextCommand):

	def run(self, edit, line, col):
		# Convert from a 1 based to a 0 based line number
		line = int(line) - 1

		# Convert from a 1 based to 0 based col number
		col = int(col) - 1

		# Negative line numbers count from the end of the buffer (file)
		if line < 0:
			lines, _ = self.view.rowcol(self.view.size())
			line = lines + line + 1

		self.moveToLineCol(line, col)

	def moveToLineCol(self, line, col):
		# Load tab_size or 4 if not defined
		s = sublime.load_settings("Preferences.sublime-settings")
		tabSize = s.get("tab_size", 4)

		# Go to first column of line
		pt = self.view.text_point(line, 0)
		self.view.sel().clear()
		self.view.sel().add(sublime.Region(pt))
		self.view.show(pt)

		colsMoved = 0
		while colsMoved < col:
			# Grab contents of next col
			nextCol = self.view.substr(pt) 
			
			# Don't move cursor beyond end of line
			if nextCol == '\n':
				print("Reached end of line!")
				break
			if nextCol == '\t' and (col - colsMoved) < tabSize:
				print("Can't reach column! (column within hard tab)")
				break 
			
			# If we're going to advance across a tab, pretend we moved no. of cols in a tab
			if nextCol == '\t':
				colsMoved += tabSize
			else:
				colsMoved += 1

			# Advance cursor
			self.view.run_command("move", {"by": "characters", "forward": True})

			# Update our record of cursors position
			pt = self.view.sel()[0].begin()