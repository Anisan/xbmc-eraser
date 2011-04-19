Parameters (separated by [B]&amp;[/B]) -

limit=#         ; # to limit returned results (default=5)
alarm=#         ; # number of minutes before running again (default=Off)

For example -
 
XBMC.RunScript(script.nextaired,limit=10&amp;alarm=30)

will return 10  episodes every 30 minutes.


Labels -

 
"NextAiredEpisode.%d.ShowTitle"
"NextAiredEpisode.%d.EpisodeTitle"
"NextAiredEpisode.%d.EpisodeNo"
"NextAiredEpisode.%d.EpisodeSeason"
"NextAiredEpisode.%d.EpisodeNumber"
"NextAiredEpisode.%d.Rating"
"NextAiredEpisode.%d.Path"
"NextAiredEpisode.%d.Fanart"
"NextAiredEpisode.%d.Thumb"
 

