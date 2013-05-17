#!/usr/local/bin/python

# Developed by Roman Arkharov, arkharov@gmail.com. 05.2013

"""
    This file is a update script for RRD monitoring tool for Quickpong server.
    Script depends on psutils and rrdtools.
"""
import urllib2
import psutil
import rrdtool

basepath = '/usr/home/pythonuser/projects/quickpong_122012/scripts/'

gamesdb = basepath + 'quickponggames.rrd'
cpudb = basepath + 'quickpongcpu.rrd'
memorydb = basepath + 'quickpongram.rrd'

gamespng = basepath + 'quickponggames.png'
cpupng = basepath + 'quickpongcpu.png'
memorypng = basepath + 'quickpongram.png'

#quickpong_stats_url = 'http://quickpong.com:10082/'
quickpong_stats_url = 'http://localhost:10082/'

pidfile = '/usr/home/pythonuser/projects/github/quickpong/twistd.pid'
f = open(pidfile, 'r+')
pid = f.read()
f.close()

data = urllib2.urlopen(quickpong_stats_url).read()
gamers, games = data.split(',')
print gamers, games
res = rrdtool.update(gamesdb, "N:" + gamers + ":" + games)
if res:
    print rrdtool.error()

rrdtool.graph(gamespng, "--start", "-1d", "--vertical-label=gamers and games",
 "DEF:gamers=" + gamesdb + ":gamers:AVERAGE:step=1",
 "DEF:games=" + gamesdb + ":games:AVERAGE:step=1",
 "AREA:games#00FF00:Games",
 "LINE1:gamers#0000FF:Gamers",
 "COMMENT:\\n",
 "GPRINT:gamers:AVERAGE:Avg gamers online\: %6.2lf",
 "COMMENT:\\n",
 "GPRINT:gamers:MAX:Max gamers online\: %6.2lf",
 "COMMENT:\\n",
 "GPRINT:gamers:LAST:Last gamers online\: %6.2lf",
 "COMMENT:\\n",
 "GPRINT:games:AVERAGE:Avg games\: %6.2lf",
 "COMMENT:\\n",
 "GPRINT:games:MAX:Max games\: %6.2lf",
 "COMMENT:\\n",
 "GPRINT:games:LAST:Last games\: %6.2lf")


p = psutil.Process(int(pid))
rss, vms = p.get_memory_info()
print rss, vms
res = rrdtool.update(memorydb, "N:" + str(rss) + ":" + str(vms))
if res:
    print rrdtool.error()

rrdtool.graph(memorypng, "--start", "-1d", "--vertical-label=rss and vms in Mb",
 "DEF:rss=" + memorydb + ":rss:AVERAGE:step=1",
 "DEF:vms=" + memorydb + ":vms:AVERAGE:step=1",
 "LINE1:rss#00FF00:RSS",
 "LINE2:vms#0000FF:VMS\\r",
 "CDEF:rssmb=rss,1048576,/",
 "CDEF:vmsmb=vms,1048576,/",
 "GPRINT:rssmb:AVERAGE:Avg RSS\: %6.2lf %SMb",
 "COMMENT:\\n",
 "GPRINT:rssmb:MAX:Max RSS\: %6.2lf %SMb",
 "COMMENT:\\n",
 "GPRINT:rssmb:LAST:Last RSS\: %6.2lf %SMb",
 "COMMENT:\\n",
 "GPRINT:vmsmb:AVERAGE:Avg VMS\: %6.2lf %SMb",
 "COMMENT:\\n",
 "GPRINT:vmsmb:MAX:Max VMS\: %6.2lf %SMb",
 "COMMENT:\\n",
 "GPRINT:vmsmb:LAST:Last VMS\: %6.2lf %SMb")



cpu_percent = p.get_cpu_percent()
print cpu_percent
res = rrdtool.update(cpudb, "N:" + str(cpu_percent))
if res:
    print rrdtool.error()

rrdtool.graph(cpupng, "--start", "-1d", "--vertical-label=CPU",
 "DEF:cpu=" + cpudb + ":cpu:AVERAGE:step=1",
 "LINE1:cpu#00FF00:CPU",
 "COMMENT:\\n",
 "GPRINT:cpu:AVERAGE:Avg CPU usage\: %6.2lf",
 "COMMENT:\\n",
 "GPRINT:cpu:MIN:Min CPU usage\: %6.2lf",
 "COMMENT:\\n",
 "GPRINT:cpu:MAX:Max CPU usage\: %6.2lf",
 "COMMENT:\\n",
 "GPRINT:cpu:LAST:Last CPU usage\: %6.2lf")

