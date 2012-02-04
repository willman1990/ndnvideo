#! /usr/bin/env python

import pygst
pygst.require("0.10")
import gst
import gobject

import pyccn

from audio_src import AudioSrc
from video_src import VideoSrc

if __name__ == '__main__':
	gobject.threads_init()

	pipeline = gst.parse_launch("queue name=vdecoder ! ffdec_h264 max-threads=3 skip-frame=5 ! autovideosink \
		queue name=adecoder ! ffdec_aac ! autoaudiosink")

	vdecoder = pipeline.get_by_name("vdecoder")
	adecoder = pipeline.get_by_name("adecoder")

	video = gst.element_factory_make("VideoSrc")
	audio = gst.element_factory_make("AudioSrc")
	video.set_property('location', '/repo/army/video')
	audio.set_property('location', '/repo/army/audio')

	pipeline.add(video, audio)
	video.link(vdecoder)
	audio.link(adecoder)

	loop = gobject.MainLoop()
	pipeline.set_state(gst.STATE_PLAYING)

	try:
		loop.run()
	except KeyboardInterrupt:
		print "Ctrl+C pressed, exitting"
		pass

	pipeline.set_state(gst.STATE_NULL)
	pipeline.get_state(gst.CLOCK_TIME_NONE)