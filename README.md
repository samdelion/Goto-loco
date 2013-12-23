Goto-loco
=========

Sublime Text plugin to go to a specified line and column.

Usage:
Edit your Preferences > Key Bindings - User file to include the following lines:

  	{ 
	  	"keys": ["ctrl+g"], 
	  	"command": "prompt_goto_lo_co" 
  	}

Replacing the "keys" field with your desired hotkey.

Input should be entered in the following format:
  
  	line<delimiter>column
  
Where "\<delimiter\>" should be replaced by 
	
	",", ":", ";", SPACE or TAB
