#
#Copyright (C) 2009  Steven J. Burch
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You may obtain a copy of this license at:
#  http://www.gnu.org/licenses/gpl-3.0.html

"""Business logic layer"""

#Standard modules
import os
#Project modules
import xbmcaddon

__settings__ = xbmcaddon.Addon(id='script.twitXBMC')
__language__ = __settings__.getLocalizedString


"""
Description:
	Appends the default footer to the status
	If necessary, mesage is truncated to fit the footer
Args:
	message::string : original status (without footer)
	maxLength::int : maximum status length (including footer)
Returns:
	string : new status (including footer), <= maxLength
"""
def appendFooterToStatus( message, maxLength, suffix ):
    status = message + " " + suffix
    if len( status ) > maxLength:
        truncator = __settings__.getSetting( "StatusTruncation" )
        status = message[ 0 : ( maxLength - len( suffix ) - len( truncator ) - 1 ) ] + truncator + " " + suffix		
    return status
	
"""
Description:
	Parses the base filename (without extension) from a path name
Args:
	file::string : the file's path
Returns:
	string : the base filename (without extension) of the path
"""
def parseTitleFromFilename( file ):
		return os.path.splitext( os.path.split( file )[ 1 ] )[ 0 ]

"""
Description:
	Strips newline characters from the input string
Args:
	text::string - input text
	[replacementString::string = " "] - string used to replace newlines
Returns:
	None if input is None
	Else, text with all newline instances replaced by the replacement string
"""
def stripNewlines( text, replacementString = " " ):
	if text is None:
		return text
	else:
		return text.replace( "\n", replacementString )