#!/usr/bin/env python
# -*- coding: utf-8 -*-
# grabber: grabs the mac screen at regular intervals
# https://github.com/bnomis/grabber
# (c) Simon Blanchard
from __future__ import print_function
import argparse
import datetime
import os
import re
import sys
import subprocess
import time
from PIL import Image, ImageDraw, ImageFont

from . import __version__


def write_log(options, log, exception=None):
    if options.dry_run:
        print(log)
        return

    try:
        with open(options.log_file, 'a') as fp:
            fp.write(log + '\n')
            if exception:
                fp.write('%s\n' % exception)
    except Exception as e:
        pass
        print('Exception writing log: %s: %s: %s' % (log, exception, e))


def run_cmd(options, argv, cwd=None):
    if options.dry_run:
        print(' '.join(argv))
        return 0

    exitcode = -1
    try:
        p = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
    except Exception as e:
        write_log(options, 'Exception running %s' % argv, exception=e)
    else:
        stdout, stderr = p.communicate()
        if stdout:
            write_log(options, stdout.decode().strip())
        if stderr:
            write_log(options, stderr.decode().strip())
        exitcode = p.wait()
    return exitcode


def grab_movie(options):
    if options.movie_day:
        d = options.movie_day
    else:
        one_day = datetime.timedelta(days=-1)
        yesterday = datetime.date.today() + one_day
        d = '%d-%02d-%02d' % (yesterday.year, yesterday.month, yesterday.day)
    
    odir = os.path.join(options.outdir, d)
    if os.path.exists(odir):
        write_log(options, 'Making movie in %s' % odir)

        argv = [
            options.ffmpeg,
            '-loglevel',
            'warning',
            '-r',
            '1/3',
            '-f',
            'image2',
            '-i',
            'grab%04d.png',
            '-s',
            'hd480',
            '-c:v',
            'libx264',
            '-b:v',
            '1000k',
            '-pix_fmt',
            'yuv420p',
            '-r',
            '25',
            '-y',
            '-pass',
            '1',
            '-passlogfile',
            'ffmpeg.log',
            'grab.mp4'
        ]
        # pass 1
        run_cmd(options, argv, cwd=odir)
        # pass 2
        argv[21] = '2'
        run_cmd(options, argv, cwd=odir)
    else:
        write_log(options, 'No movie to be made in %s' % odir)


def timestamp(options, path):
    im = Image.open(path)
    draw = ImageDraw.Draw(im)
    now = datetime.datetime.now()
    stamp = '%02d:%02d' % (now.hour, now.minute)
    width, height = options.font.getsize(stamp)
    draw.rectangle([(0, 0), (width, height)], fill='black')
    draw.text((0, 0), stamp, font=options.font, fill='white')
    im.save(path)


def loginwindow_pid(options):
    try:
        lines = subprocess.Popen(['ps', '-ax'], stdout=subprocess.PIPE).communicate()[0]
    except Exception as e:
        write_log(options, 'Exception getting loginwindow pid', exception=e)
    else:
        for l in lines.split('\n'):
            if l.find('loginwindow') != -1:
                l = l.strip()
                return l.split()[0]
    return 0


def parse_time(tmstr):
    pattern = r'(?P<hours>[0-9][0-9]):(?P<mins>[0-9][0-9])'
    mo = re.match(pattern, tmstr)
    hours = int(mo.group(1))
    minutes = int(mo.group(2))
    t = datetime.time(hours, minutes)
    return t


def wait_until(options):
    f = parse_time(options.frmtm)
    t = parse_time(options.totm)
    n = datetime.datetime.now().time()
    while (n < f) or (n > t):
        time.sleep(30)
        n = datetime.datetime.now().time()


def make_odir(options):
    today = datetime.date.today()
    d = '%d-%02d-%02d' % (today.year, today.month, today.day)
    odir = os.path.join(options.outdir, d)
    if not os.path.exists(odir):
        try:
            os.makedirs(odir)
        except Exception as e:
            write_log(options, 'Exception making directory %s' % odir, exception=e)
    return odir


def check_odir(options, odir):
    try:
        ls = os.listdir(odir)
    except Exception as e:
        write_log(options, 'Exception listing directory %s' % odir, exception=e)
        return 0

    num_files = len(ls)
    count = 1
    if num_files > 0:
        ls.sort()
        last = ls[-1]
        pattern = r'%s(?P<cnt>[0-9][0-9][0-9][0-9])\.png' % options.base
        mo = re.match(pattern, last)
        count = int(mo.group(1)) + 1
    return count


def grab(options):
    # make sure the output directory exists before we write into it
    # because maybe it has disappeared or been deleted by the user
    # for example to make space (this is a long runnning program)
    odir = make_odir(options)
    count = check_odir(options, odir)
    fname = '%s%04d.png' % (options.base, count)
    path = os.path.join(odir, fname)
    pid = loginwindow_pid(options)
    if pid:
        args = [
            'launchctl',
            'bsexec',
            pid,
            'screencapture',
            '-C',
            '-m',
            '-x',
            path
        ]
        exitcode = run_cmd(options, args)
        if exitcode == 0 and os.path.exists(path):
            timestamp(options, path)


def grab_loop(options):
    if options.frmtm:
        wait_until(options)
    if options.totm:
        quitime = parse_time(options.totm)
    today = datetime.date.today()
    write_log(options, 'Grabbing from %s to %s' % (options.frmtm, options.totm))
    while 1:
        grab(options)
        if options.totm:
            # it's possible we slept through the night
            if (datetime.datetime.now().time() > quitime) or (datetime.date.today() != today):
                break
        time.sleep(options.repeat * 60)


def grab_once(options):
    grab(options)


def grabber(options):
    if options.movie or options.movie_day:
        return grab_movie(options)

    if options.once:
        grab_once(options)
    else:
        # loop forever
        if options.frmtm and options.totm:
            while 1:
                grab_loop(options)
        else:
            grab_loop(options)
    return 0


def parse_opts(argv):
    program_name = 'grabber'
    usage_string = '%(prog)s [options]'
    version_string = '%(prog)s %(version)s' % {'prog': program_name, 'version': __version__}
    description_string = 'grabber: periodically grabs a copy of the screen'

    pwd = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    fontpath = os.path.join(pwd, 'fonts/SourceCodePro-Regular.otf')

    parser = argparse.ArgumentParser(
        prog=program_name,
        usage=usage_string,
        description=description_string,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--version',
        action='version',
        version=version_string
    )

    parser.add_argument(
        '--dry-run',
        dest='dry_run',
        action='store_true',
        default=False,
        help='Do nothing but print what would be done. Default: %(default)s.'
    )

    parser.add_argument(
        '--log-file',
        default='/var/root/logs/grabber.log',
        help='File to write logs to. Default: %(default)s.'
    )

    parser.add_argument(
        '-b',
        '--base',
        default='grab',
        help='Base file name. Default: %(default)s.',
    )

    parser.add_argument(
        '-d',
        '--directory',
        dest='outdir',
        default='/var/root/grabs',
        help='Parent directory to store grabs to. Default: %(default)s.'
    )

    parser.add_argument(
        '--fontpath',
        default=fontpath,
        help='Path to font to use for time stamps. Default: %(default)s.'
    )

    parser.add_argument(
        '-r',
        '--repeat',
        default=5,
        type=int,
        help='Repeat in minutes. Default: %(default)s.',
    )

    parser.add_argument(
        '-f',
        '--from',
        dest='frmtm',
        default='08:30',
        help='From time. 24-hour format with a leading zero if needed. Default: %(default)s.'
    )

    parser.add_argument(
        '-t',
        '--to',
        dest='totm',
        default='20:00',
        help='To time. 24-hour format with a leading zero if needed. Default: %(default)s.'
    )

    parser.add_argument(
        '--once',
        default=False,
        action='store_true',
        help='Run once. Default: %(default)s.'
    )

    parser.add_argument(
        '--movie',
        default=False,
        action='store_true',
        help='Make the movie for the previous day. Default: %(default)s.'
    )

    parser.add_argument(
        '--movie-day',
        metavar='YYYY-MM-DD',
        help='Make the movie for a specified day. Specified as YYYY-MM-DD.'
    )

    parser.add_argument(
        '--ffmpeg',
        default='/opt/local/bin/ffmpeg',
        help='Path to the ffmpeg command.'
    )

    options = parser.parse_args(argv)

    options.font = ImageFont.truetype(filename=options.fontpath, size=128)
    return options


def main(argv):
    rv = 1
    options = parse_opts(argv)
    try:
        rv = grabber(options)
    except Exception as e:
        write_log(options, 'Grabber exception', exception=e)
    return rv


def run():
    sys.exit(main(sys.argv[1:]))


if __name__ == '__main__':
    run()

