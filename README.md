# grabber

Periodically grab a picture of your Mac's screen and optionally make a movie of the grabs.

By default, runs the Mac's `screencapture` utility every 5 minutes and saves the grab into `/var/root/grabs/YYYY-MM-DD/grabNNNN.png`.

## Making Movies

The script uses `ffmpeg` to make movies. Specify the path to `ffmpeg` using the --ffmpeg option to the script.

To make a movie of the previous day's grabs run:

```shell
$ grabber [your-normal-grabber-options] --movie
```

To make a movie of a specific day's grabs run:

```shell
$ grabber [your-normal-grabber-options] --movie-day YYYY-MM-DD
```

When making a movie pass in the same options you used to create the grabs. Just add --movie on the end of the options. This is so the script knows where the grabs were stored. Note: you may need to specify the path the `ffmpeg`.

The movie is placed in to the same directory as the grabs, named `grab.mp4`.

If you wish to make a movie every day, you can use the supplied launchd file `launchd/com.yajogo.grabber.movie.plist`. Installing this (symlink to `/Library/LaunchDaemons` and `launchctl load -w`) will launch grabber just after midnight every day to make the movie for the previous day.


## Utilities

Several utilities are provided with the script...

* `enc.sh` is a shell script that can be run in a directory containing grabbed PNG files to produce a movie of the grabs.
* `seq.py` will uniformly re-name files in ascending order, suitable for making movies. This really only useful for development.

## Usage

```shell
usage: grabber [options]

grabber: periodically grabs a copy of the screen

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --dry-run             Do nothing but print what would be done. Default:
                        False.
  --log-file LOG_FILE   File to write logs to. Default:
                        /var/root/logs/grabber.log.
  -b BASE, --base BASE  Base file name. Default: grab.
  -d OUTDIR, --directory OUTDIR
                        Parent directory to store grabs to. Default:
                        /var/root/grabs.
  --fontpath FONTPATH   Path to font to use for time stamps. Default:
                        /Users/simonb/src/grabber/fonts/SourceCodePro-
                        Regular.otf.
  -r REPEAT, --repeat REPEAT
                        Repeat in minutes. Default: 5.
  -f FRMTM, --from FRMTM
                        From time. 24-hour format with a leading zero if
                        needed. Default: 08:30.
  -t TOTM, --to TOTM    To time. 24-hour format with a leading zero if needed.
                        Default: 20:00.
  --once                Run once. Default: False.
  --movie               Make the movie for the previous day. Default: False.
  --movie-day YYYY-MM-DD
                        Make the movie for a specified day. Specified as YYYY-
                        MM-DD.
  --ffmpeg FFMPEG       Path to the ffmpeg command.
```

## Fonts

The script, by default, uses the supplied [Source Code Pro][scp] font from Adobe to write a time stamp on the screen grab. You can change the font using the --fontpath option. I suggest you use a mono-spaced font so the time stamp does not grow and shrink over time.

[scp]: https://github.com/adobe-fonts/source-code-pro

## Install

The script needs to be run as root. So, before you install become root.

The script requires Pillow to time stamp the screen grabs, so you may as well create a virtualenv first and then pip install.

Suggested install steps are:

1. Create a virtualenv
2. `pip install grabbber` in the new virtualenv
3. Edit the launchd file `launchd/com.yajogo.grabber.plist` to suit
4. Run `bin/install.py`. This will symlink `com.yajogo.grabber.plist` in to `/Library/LaunchDaemons` and load the file in to launchd.

## Uninstall

As root.

Either:

* run the `bin/uninstall.py` script. 

Or: 

* manually unload from `launchd` and delete the symlink in `/Library/LaunchDaemons`.

