#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging

logging.basicConfig(level=logging.WARN, format='%(levelname)-8s %(message)s')
logger = logging.getLogger('hack-clock')

os.chdir(os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from dateutil import parser
from datetime import datetime
from config import configuration
from clock import Clock, ProcessStatus
from bottle import Bottle, HTTPResponse, static_file, get, put, request, response, redirect, template
from os import listdir

application = Bottle()
application.install(Clock())

@application.route('/favicon.ico')
def send_favicon():
    return static_file('favicon.ico', root='views/images')

@application.route('/js/<filename:path>')
def send_js(filename):
    return static_file(filename, root='views/js')

@application.route('/css/<filename:path>')
def send_css(filename):
    return static_file(filename, root='views/css')

@application.get('/')
def editor():
    return template('index')

@application.route('/codemirror/<filename:path>')
def send_js(filename):
    return static_file(filename, root='views/codemirror')

@application.post('/clock/restart')
def restart_event_loop(clock):
    clock.restart()
    return '{ "status": "restarted" }'

@application.get('/clock/status')
def status_event_loop(clock):
    return '{ "status": "%s" }' % clock.status()

@application.get('/clock/failures')
def status_stderr(clock):
    return clock.failures()

@application.get('/clock/code')
def edit_event_loop(clock):
    code_file = open(clock.sourceFile, 'r')
    return template('editor', code=code_file.read(), status="Opened")

@application.post('/clock/code')
def save_event_loop(clock):
    version_dir = configuration.get('backup_files')
    backup_name = "%s/run_clock.%s" % (version_dir, datetime.now().isoformat())

    try:
        # Save backup
        code_file = open(clock.sourceFile, 'r')
        backup_file = open(backup_name, 'w')
        backup_file.write(code_file.read())

        # Save file
        code_file = open(clock.sourceFile, 'w')
        code_file.write(request.forms.get('code'))

        clock.restart()

        # Load saved file
        code_file = open(clock.sourceFile, 'r')
        return template('editor', code=code_file.read(), status="Saved")
    except:
        return template('editor', code=request.forms.get('code'), status="Failed")

@application.post('/audio')
def audio_upload():
    uploaded = request.files.get('upload')
    audio_dir = configuration.get('audio_files')
    uploaded.save(audio_dir)
    redirect("/audio")

@application.get('/audio')
def audio_list():
    audio_dir = configuration.get('audio_files')
    files = listdir(audio_dir)
    return template('audio', files=files)

@application.get('/clock/code/backups')
def backup_list(clock):
    version_dir = configuration.get('backup_files')
    files = listdir(version_dir)

    backups = []
    for filename in files:
        backup_name = "%s/%s" % (version_dir, filename)
        diff = open(backup_name, 'r').read()

        filetime = parser.parse(filename.lstrip("run_clock."))
        backups.append((filetime.strftime("%s"), filetime.strftime("%Y-%m-%d"), filetime.strftime("%H:%M:%S"), diff, filename))

    return template('backups', backups=backups)

@application.put('/clock/code/restore')
def restore_event_loop(clock):
    uploaded = request.file.get('id')
    version_dir = configuration.get('backup_files')
    files = listdir(version_dir)
    # Find the file we need to restore

    try:
        # Load saved file
        code_file = open(restored_file, 'r')
        return template('editor', code=code_file.read(), status="Saved")
    except:
        return template('editor', code=request.forms.get('code'), status="Failed")
