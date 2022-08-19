#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, redirect, request, Response, send_file, send_from_directory
from flask_restful import Api, Resource, abort
from webargs import fields, validate
from webargs.flaskparser import use_args, use_kwargs, parser, abort
import glob, os, shlex, subprocess
from os import path
from datetime import datetime

app = Flask(__name__)
api = Api(app)

allowed_commands = [
    'curl',
    'dig',
    'mtr',
    'nslookup',
    'phantomjs',
    'ping',
    'traceroute',
    ]

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/shellinabox')
def shellinabox():
    # Use shellinabox server for this environment
    shellinabox_server = 'http://shellinabox.microverse.' + os.environ['BUILD_ENV'] + '.inspcloud.com/'
    return redirect(shellinabox_server)

@parser.error_handler
def handle_request_parsing_error(err):
    abort(422, errors=err.messages)

def abort_if_command_not_allowed(command):
    if command not in allowed_commands:
        abort(404, message='Command {} not allowed'.format(command))

class ShellCommand(Resource):

    args = {'command': fields.Str(required=True),
            'parameters': fields.Str(required=True)}

    def process_commands(self, command, parameters):
        
        abort_if_command_not_allowed(command)

        if command == 'ping':
            ping_options = ['-a','-A','-b','-B','-c','-d','-F','-f', '-i','-I','-l','-L','-n','-p','-q','-Q','-R','-r','-s','-S','-t','-T','-M','-U','-V']
            ping_args = shlex.split(parameters)
            if ping_args[0] not in ping_options:
                return ('Invalid ping option.')

        if command == 'phantomjs':
            timestamp = datetime.today().strftime('%Y%m%d%H%M%S')
            screenshot_path = '/opt/microverse/net-tools/app/static/screenshot/'
            screenshot_name = 'screenshot_' + timestamp + '.png'
            screenshot = screenshot_path + screenshot_name
            old_screenshot = glob.glob(screenshot_path + 'screenshot*.png')
            if old_screenshot:
                if os.path.isfile(old_screenshot[0]):
                    os.remove(old_screenshot[0])
            command_line = 'phantomjs --ignore-ssl-errors=true --ssl-protocol=any /opt/microverse/net-tools/app/screenshot.js ' + parameters +  ' ' + screenshot
            process_args = shlex.split(command_line)
            output = subprocess.check_output(process_args, shell=False, stderr=subprocess.STDOUT)
            resp = send_from_directory(screenshot_path, screenshot_name, as_attachment=True, mimetype='application/octet-stream')
        else:
            command_line = command + ' ' + parameters
            process_args = shlex.split(command_line)
            output = subprocess.check_output(process_args, shell=False, stderr=subprocess.STDOUT)
            resp = Response(output, mimetype='text/plain', headers=None)
            resp.status = 'code=200'
        return resp

    @use_kwargs(args)
    def get(self, command, parameters):
        results = ShellCommand.process_commands(self, command, parameters)
        return results

    @use_kwargs(args)
    def post(self, command, parameters):
        results = ShellCommand.process_commands(self, command, parameters)
        return results

api.add_resource(ShellCommand, '/shellcommand')

if __name__ == '__main__':
    # Disable debug in production
    # app.run(debug=True, host='0.0.0.0')
    app.run(host='0.0.0.0')
