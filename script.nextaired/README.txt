Parameters (separated by [B]&amp;[/B]) -

limit=#         ; # to limit returned results (default=5)
alarm=#         ; # number of minutes before running again (default=Off)

For example -
 
XBMC.RunScript(script.nextaired,limit=10&amp;alarm=30)

will return 10 episodes  every 30 minutes.


Labels -

"NextAiredEpisode.%d.Title"
"NextAiredEpisode.%d.Rating"
"NextAiredEpisode.%d.Year"
"NextAiredEpisode.%d.RunningTime"
"NextAiredEpisode.%d.Path"
"NextAiredEpisode.%d.Trailer"
"NextAiredEpisode.%d.Fanart"
"NextAiredEpisode.%d.Thumb"
 
