#!/usr/bin/env python3

import os
import json
import subprocess

group_member = 'sysadmin'
userlist = {group_member: []}
outputfile = '/'.join(["/tmp", group_member]) + ".json"

def get_chef_repo():

	 config = subprocess.Popen('knife config get cookbook_path -F json', shell=True, stdout=subprocess.PIPE).communicate()

	 if config[0]:
	 	chef_repo = os.path.split(json.loads(config[0].decode('utf-8'))['cookbook_path'][0])[0]

	 return chef_repo


users_databag = '/'.join([get_chef_repo(),'data_bags/users/'])

for file in sorted(os.listdir(users_databag)):	
	if file.endswith('.json'):
		with open('/'.join([users_databag, file]), 'rb') as userfile:			
			userdata = json.load(userfile)
			userfile.close()

			if 'groups' in userdata.keys() and group_member in userdata['groups']:
				if len(userdata['ssh_keys']) > 0:
					ssh_keys = userdata['ssh_keys'][0]
				else:
					ssh_keys = []

				user = { "name": userdata['id'],
						 "uid": userdata['uid'],
						 "shell": userdata['shell'],
						 "comment": userdata['comment'],
						 "ssh_keys": ssh_keys,
						 "action": userdata['action']
					   }
				userlist[group_member].append(user)

with open(outputfile, 'w') as output:
    json.dump(userlist, output)
    output.close()