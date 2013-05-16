# Developed by Roman Arkharov, arkharov@gmail.com. 05.2013

"""
    This file is a setup script for RRD monitoring tool for Quickpong server.
"""
import rrdtool

rrdtool.create("quickponggames.rrd", "--step", "60", "--start", '0',
 "DS:gamers:GAUGE:120:U:U",
 "DS:games:GAUGE:120:U:U",
 "RRA:AVERAGE:0.5:1:525600",
 "RRA:AVERAGE:0.5:15:35040",
 "RRA:AVERAGE:0.5:30:17520",
 "RRA:AVERAGE:0.5:60:8760",
 "RRA:MIN:0.5:1:525600",
 "RRA:MIN:0.5:15:35040",
 "RRA:MIN:0.5:30:17520",
 "RRA:MIN:0.5:60:8760",
 "RRA:MAX:0.5:1:525600",
 "RRA:MAX:0.5:15:35040",
 "RRA:MAX:0.5:30:17520",
 "RRA:MAX:0.5:60:8760")


rrdtool.create("quickpongram.rrd", "--step", "60", "--start", '0',
 "DS:rss:GAUGE:120:U:U",
 "DS:vms:GAUGE:120:U:U",
 "RRA:AVERAGE:0.5:1:525600",
 "RRA:AVERAGE:0.5:15:35040",
 "RRA:AVERAGE:0.5:30:17520",
 "RRA:AVERAGE:0.5:60:8760",
 "RRA:MIN:0.5:1:525600",
 "RRA:MIN:0.5:15:35040",
 "RRA:MIN:0.5:30:17520",
 "RRA:MIN:0.5:60:8760",
 "RRA:MAX:0.5:1:525600",
 "RRA:MAX:0.5:15:35040",
 "RRA:MAX:0.5:30:17520",
 "RRA:MAX:0.5:60:8760")


rrdtool.create("quickpongcpu.rrd", "--step", "60", "--start", '0',
 "DS:cpu:GAUGE:120:U:U",
 "RRA:AVERAGE:0.5:1:525600",
 "RRA:AVERAGE:0.5:15:35040",
 "RRA:AVERAGE:0.5:30:17520",
 "RRA:AVERAGE:0.5:60:8760",
 "RRA:MIN:0.5:1:525600",
 "RRA:MIN:0.5:15:35040",
 "RRA:MIN:0.5:30:17520",
 "RRA:MIN:0.5:60:8760",
 "RRA:MAX:0.5:1:525600",
 "RRA:MAX:0.5:15:35040",
 "RRA:MAX:0.5:30:17520",
 "RRA:MAX:0.5:60:8760")
