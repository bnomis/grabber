#!/bin/sh
# input: images at a (virtual) 3 frames per second
# output: MPEG4 852x480 1.8Mbits 25 frames per second
# encoding: two pass, overwrite output files
ffmpeg -loglevel warning -r 1/3 -f image2 -i grab%04d.png -s hd480 -vcodec mpeg4 -b:v 1800000 -r 25 -y -pass 1 -passlogfile ffmpeg.log grab.mp4
ffmpeg -loglevel warning -r 1/3 -f image2 -i grab%04d.png -s hd480 -vcodec mpeg4 -b:v 1800000 -r 25 -y -pass 2 -passlogfile ffmpeg.log grab.mp4
