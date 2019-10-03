#!/usr/bin/env python3

import json
import subprocess


def shell_cmd(cmd):

	command = subprocess.Popen(cmd, shell=True, executable='/bin/bash')
	command.wait()
	return command.returncode


userlist = json.load(open('/tmp/sysadmin.json', 'r'))

for user in userlist['sysadmin']:
	name = user['name']
	uid = user['uid']
	shell = user['shell']
	comment = user['comment']
	ssh_keys = user['ssh_keys']
	action = user['action']

	if action == 'create' and len(ssh_keys) > 0:
		useradd = shell_cmd('useradd -m ' + name + ' -u ' + str(uid) + ' -G sysadmin -s ' + shell + ' -c "' + comment + '"')
		if useradd == 0:
			mkdir = shell_cmd('mkdir -p /home/' + name + '/.ssh/')
			if mkdir == 0:
				with open('/home/' + name + '/.ssh/authorized_keys', 'w') as authorized_keys:
					authorized_keys.write(user['ssh_keys'])
					authorized_keys.close()
					chmod = shell_cmd('chmod 600 /home/' + name + '/.ssh/authorized_keys')
					if chmod == 0:				
						chown = shell_cmd('chown ' + name + ':' + name + ' -R /home/' + name + '/.ssh/')

	if action == 'remove':
		userdel = shell_cmd('userdel -rf ' + name + ' > /dev/null 2>&1')