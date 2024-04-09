#
# This file is part of nzbget. See <https://nzbget.com>.
#
# Copyright (C) 2024 Denis <denis@nzbget.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#


import os
import sys
import urllib.parse
import urllib.request
import json
from json import JSONDecodeError

SUCCESS = 93
ERROR = 94
NONE = 95

METHODS_MAP = {
	'Copy': 'copy',
	'Move': 'move',
	'Hard Link': 'hardlink',
	'Symbolic Link': 'symlink',
}

REQUIRED_OPTIONS = [
	'NZBPO_APIKEY',
	'NZBPO_HOST',
	'NZBPO_PORT',
	'NZBPO_PROCESSMETHOD',
	'NZBPO_FORCEREPLACE',
	'NZBPO_ISPRIORITY',
	'NZBPO_VERBOSE',
]

def validate_options(options: list, methods_map: dict) -> None:
	for	optname in options:
		if (not optname in os.environ):
			print(f'[ERROR] Option {optname[6:]} is missing in configuration file. Please check extension settings.')
			sys.exit(ERROR)
	
	method = os.environ.get('NZBPO_PROCESSMETHOD')
	if method == None or methods_map.get(method) == None:
		print(f'[ERROR] Unsupported process method: {method}.')
		sys.exit(ERROR)

	if not os.environ.get('NZBCP_COMMAND') and not os.environ.get('NZBPP_DIRECTORY') and not os.environ.get('NZBPP_FINALDIR'):
		print(f'[ERROR] The path to the downloaded file is not provided.')
		sys.exit(ERROR)


validate_options(REQUIRED_OPTIONS, METHODS_MAP)


API_KEY = os.environ['NZBPO_APIKEY']
HOST = os.environ['NZBPO_HOST']
PORT = os.environ['NZBPO_PORT']
PATH = os.environ.get('NZBPP_FINALDIR') or os.environ['NZBPP_DIRECTORY']
PROCESS_METHOD = METHODS_MAP[os.environ['NZBPO_PROCESSMETHOD']]
FORCE_REPLACE = int(os.environ['NZBPO_FORCEREPLACE'] == 'yes')
IS_PRIORITY = int(os.environ['NZBPO_ISPRIORITY'] == 'yes')
VERBOSE = os.environ['NZBPO_VERBOSE'] == 'yes'
COMMAND = os.environ.get('NZBCP_COMMAND') == 'ping'

URL = f'http://{HOST}:{PORT}/api/{API_KEY}'

if VERBOSE: 
	print('[INFO] URL:', URL)
	print('[INFO] PATH:', PATH)

def ping_sickchill(url: str) -> int:
	try:
		encoded_params = urllib.parse.urlencode({ 'cmd': 'sb.ping' })

		if VERBOSE:
			print(f'[INFO] PARAMS:', encoded_params)

		full_url = f'{url}?{encoded_params}'
		with urllib.request.urlopen(full_url) as response:
			data = response.read().decode('utf-8')
			response_dict = json.loads(data)

			if response_dict['result'] == 'success':
				print('[INFO] SickChill pinged successfully:', response_dict['message'])
				return SUCCESS

			print('[ERROR] Couldn\'t ping:', response_dict['message'])
			return ERROR
	
	except JSONDecodeError as ex:
		print('[ERROR] Wrong API Key?')
		return ERROR

	except Exception as ex:
		print('[ERROR] Unexpected exception:', ex)
		return ERROR
	
def start_post_proccessing(url: str, path: str, process_method: str, force_replace: int, is_priority: int) -> int:
	try:
		encoded_params = urllib.parse.urlencode({
			'cmd': 'postprocess',
			'path': path,
			'process_method': process_method,
			'force_replace': force_replace,
			'is_priority': is_priority,
		})

		if VERBOSE:
			print(f'[INFO] PARAMS:', encoded_params)

		full_url = f'{url}?{encoded_params}'
		with urllib.request.urlopen(full_url) as response:
			data = response.read().decode('utf-8')
			response_dict = json.loads(data)

			if response_dict['result'] == 'success':
				print('[INFO] Post-processing started successfully:', response_dict['message'])
				return SUCCESS

			print('[ERROR] Couldn\'t start Post-processing:', response_dict['message'])
			return ERROR

	except JSONDecodeError as ex:
		print('[ERROR] Wrong API Key?')

	except Exception as ex:
		print('[ERROR] Unexpected exception:', ex)
		return ERROR


if COMMAND:
	sys.exit(ping_sickchill(URL))

sys.exit(
	start_post_proccessing(
		URL, 
		PATH, 
		PROCESS_METHOD, 
		FORCE_REPLACE,
		IS_PRIORITY,
	)
)
