#!/usr/bin/env python

from twisted.internet import reactor
import sys
import functools

import txtorcon


try:
    import stem
except ImportError:
    print "This example requires Stem to be installed (or at least importable)"
    sys.exit(1)


def received_stem_event(event_type, data):
    e = txtorcon.create_stem_event(event_type, data)
    print "Stem event:", type(e)
    import stem.response.events
    if issubclass(type(e), stem.response.events.LogEvent):
        print e.message


def setup(proto):
    print "Connected to a Tor version", proto.version
    for event in ['INFO', 'NOTICE', 'WARN', 'ERR']:
        proto.add_event_listener(event, functools.partial(received_stem_event, event))


def setup_failed(arg):
    print "SETUP FAILED", arg
    reactor.stop()

d = txtorcon.build_local_tor_connection(reactor, build_state=False)
d.addCallback(setup).addErrback(setup_failed)
reactor.run()