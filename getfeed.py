#!/usr/bin/env python
__version__ = "0.1+"
__license__ = "BSD-4"
__author__ = "Sergei Shilovsky <triumhiz@yandex.ru>"

from sys import stderr
from os import path
import argparse
from pprint import pprint

import yaml
import xdg.BaseDirectory as xdgbase
import feedparser

DEFAULT_CONFIG = "config.yaml"
PROJECT_NAME = "getfeed"
DROP_NONE = "None"

def err(msg):
    print >> stderr, "ERROR: ", msg
    exit(255)

def warn(msg):
    print >> stderr, "WARNING: ", msg

def info(msg):
    print "INFO: ",msg

### Configuration parsing

def get_config(configfile=None):
    if configfile is None:
        configfile = DEFAULT_CONFIG

    in_configfile = configfile
    
    if path.sep not in configfile:
        configfile = xdgbase.load_first_config(
                path.join(PROJECT_NAME,configfile))

    if configfile is None:
        warn('File "%s" not found'%in_configfile)
    
    try:
        f = None
        f = open(configfile)
        return yaml.load(f)
    except:
        warn('Error loading/parsing "%s"'%in_configfile)
    finally:
        if f is not None:
            f.close()

def extract_records(config,key,req_type):
    # TODO normal error and warning messages
    l = config.get(key)
    t = type(l)
    if t is not req_type and l is not None:
        err('%s expected for "%s" key'%(req_type.__name__,key))
    if l is None or len(l) == 0:
        warn('empty %s for "%s" key'%(req_type.__name__,key))

    return l

def parse_config(config):
    if config is None:
        return
    if type(config) is not dict:
        err('Config file is not a dictionary')

    drops = extract_records(config,'drops',dict)
    feeds = extract_records(config,'feeds',list)

    for i, feed in enumerate(feeds,start=1):
        if type(feed) is not dict:
            err('dict expected for feeds record element')
        drop_name = feed.get('drop','default')
        if drop_name == DROP_NONE:
            drop = None
        else:
            drop = drops.get(drop_name,None)
            if drop is None:
                warn(('Drop record "%s" for feed #%s not found.\n'+
                    'Supposing "%s"')
                        % (drop_name, i, DROP_NONE))
        feed["drop"] = drop
        yield feed
   

### Arguments parsing
argparser = argparse.ArgumentParser(description=
        'RSS/Atom feed fetcher and piper')
argparser.add_argument('--version',action='version',
        version='%(prog)s '+__version__)
argparser.add_argument('--rcfile','-r',action='append',
        help='use this config file instead of default one. '+
        'You may use this option more than once.')

def main():
    args = argparser.parse_args()
    rcfiles = args.rcfile
    if rcfiles is None or len(rcfiles) == 0:
        rcfiles = (None,)

    for rc in rcfiles:
        conf = get_config(rc)
        feeds = parse_config(conf)
        for feed in feeds:
            process_feed(feed)

### Feed parsing

def process_feed(feed):
    pprint(feed)
    url = feed.get('url')
    if url is None:
        warn("Feed without URL specified")
        return
    d = feedparser.parse(url)
    # TODO

if __name__ == '__main__':
    main()

