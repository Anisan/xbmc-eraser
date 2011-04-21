import xbmc
import xbmcgui
from urllib import quote_plus, unquote_plus
import re
import sys
import os
import random


class Main:
    # grab the home window
    WINDOW = xbmcgui.Window( 10000 )

    def _clear_properties( self ):
        # we enumerate thru and clear individual properties in case other scripts set window properties
        for count in range( self.LIMIT ):
            # we clear title for visible condition
            self.WINDOW.clearProperty( "NextAiredEpisode.%d.ShowTitle" % ( count + 1, ) )
            self.WINDOW.clearProperty( "NextAiredEpisode.%d.EpisodeTitle" % ( count + 1, ) )
            self.WINDOW.clearProperty( "NextAiredEpisode.%d.EpisodeNo" % ( count + 1, ) )
            self.WINDOW.clearProperty( "NextAiredEpisode.%d.Path" % ( count + 1, ) )
            
            
    def _get_media( self, path, file ):
        # set default values
        play_path = fanart_path = thumb_path = path + file
        # we handle stack:// media special
        if ( file.startswith( "stack://" ) ):
            play_path = fanart_path = file
            thumb_path = file[ 8 : ].split( " , " )[ 0 ]
        # we handle rar:// and zip:// media special
        if ( file.startswith( "rar://" ) or file.startswith( "zip://" ) ):
            play_path = fanart_path = thumb_path = file
        # return media info
        return xbmc.getCacheThumbName( thumb_path ), xbmc.getCacheThumbName( fanart_path ), play_path

    def _parse_argv( self ):
        try:
            # parse sys.argv for params
            params = dict( arg.split( "=" ) for arg in sys.argv[ 1 ].split( "&" ) )
        except:
            # no params passed
            params = {}
        # set our preferences
        self.LIMIT = int( params.get( "limit", "5" ) )
        self.ALARM = int( params.get( "alarm", "0" ) )
        
    def _set_alarm( self ):
        # only run if user/skinner preference
        if ( not self.ALARM ): return
        # set the alarms command
        command = "XBMC.RunScript(%s,limit=%d&alarm=%d)" % ( os.path.join( os.getcwd(), __file__ ), self.LIMIT, self.ALARM, )
        xbmc.executebuiltin( "AlarmClock(RandomItems,%s,%d,true)" % ( command, self.ALARM, ) )

    def __init__( self ):
        # parse argv for any preferences
        self._parse_argv()
        # format our records start and end
        xbmc.executehttpapi( "SetResponseFormat()" )
        xbmc.executehttpapi( "SetResponseFormat(OpenRecord,%s)" % ( "<record>", ) )
        xbmc.executehttpapi( "SetResponseFormat(CloseRecord,%s)" % ( "</record>", ) )
        # clear properties
        self._clear_properties()
        # set any alarm
        self._set_alarm()
        # fetch media info
        self._fetch_tvshow_info()
    
    def _fetch_tvshow_info( self ):
        # set our unplayed query
        unplayed = "where playCount is null "
        # sql statement
        # tv shows not finished
        sql_episodes = "select episodeview.* from episodeview %s order by episodeview.idShow, episodeview.c12, episodeview.strFileName  " % ( unplayed, )
        # query the database
        episodes_xml = xbmc.executehttpapi( "QueryVideoDatabase(%s)" % quote_plus( sql_episodes ), )
        # separate the records
        episodes = re.findall( "<record>(.+?)</record>", episodes_xml, re.DOTALL )
        # enumerate thru our records and set our properties
        cShows = 0
        idShows = [ 0 ] * 8
        for count,episode in enumerate( episodes ):
            # separate individual fields
            fields = re.findall( "<field>(.*?)</field>", episode, re.DOTALL )
            if (cShows < self.LIMIT):
              if (fields[31] not in idShows):
                idShows[cShows] = fields[31]
                # set properties        
                self.WINDOW.setProperty( "NextAiredEpisode.%d.ShowTitle" % ( cShows + 1, ), fields[ 29 ] )
                self.WINDOW.setProperty( "NextAiredEpisode.%d.EpisodeTitle" % ( cShows + 1, ), fields[ 2 ] )
                self.WINDOW.setProperty( "NextAiredEpisode.%d.EpisodeNo" % ( cShows + 1, ), "s%02de%02d" % ( int( fields[ 14 ] ), int( fields[ 15 ] ), ) )
                self.WINDOW.setProperty( "NextAiredEpisode.%d.EpisodeSeason" % ( cShows + 1, ), fields[ 14 ] )
                self.WINDOW.setProperty( "NextAiredEpisode.%d.EpisodeNumber" % ( cShows + 1, ), fields[ 15 ] )
                self.WINDOW.setProperty( "NextAiredEpisode.%d.Rating" % ( cShows + 1, ), "%.1f" % float(fields[ 5 ]) )
                self.WINDOW.setProperty( "NextAiredEpisode.%d.Plot" % ( cShows + 1, ), fields[ 3 ] )
                # get cache names of path to use for thumbnail/fanart and play path
                thumb_cache, fanart_cache, play_path = self._get_media( fields[ 26 ], fields[ 25 ] )
                if ( not os.path.isfile( xbmc.translatePath( "special://profile/Thumbnails/Video/%s/%s" % ( "Fanart", fanart_cache, ) ) ) ):
                    fanart_cache = xbmc.getCacheThumbName(os.path.join(os.path.split(os.path.split(fields[ 25 ])[0])[0], ""))
                if os.path.isfile("%s.dds" % (xbmc.translatePath( "special://profile/Thumbnails/Video/%s/%s" % ( "Fanart", os.path.splitext(fanart_cache)[0],) ) )):
                    fanart_cache = "%s.dds" % (os.path.splitext(fanart_cache)[0],)
                self.WINDOW.setProperty( "NextAiredEpisode.%d.Path" % ( cShows + 1, ), play_path )
                self.WINDOW.setProperty( "NextAiredEpisode.%d.Fanart" % ( cShows + 1, ), "special://profile/Thumbnails/Video/%s/%s" % ( "Fanart", fanart_cache, ) )
                # initial thumb path
                thumb = "special://profile/Thumbnails/Video/%s/%s" % ( thumb_cache[ 0 ], thumb_cache, )
                # if thumb does not exist use an auto generated thumb path
                if ( not os.path.isfile( xbmc.translatePath( thumb ) ) ):
                    thumb = "special://profile/Thumbnails/Video/%s/auto-%s" % ( thumb_cache[ 0 ], thumb_cache, )
                self.WINDOW.setProperty( "NextAiredEpisode.%d.Thumb" % ( cShows + 1, ), thumb )
                cShows = cShows + 1
 
if ( __name__ == "__main__" ):
    Main()
