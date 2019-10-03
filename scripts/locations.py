#!/usr/bin/env python3

import argparse
import configparser


def create_location(config, location_name, data, inifile):

	config['locations'][str(len(config['locations']))] = location_name

	for section in data.keys():
		config[section] = {}

		for key in data[section].keys():
			config[section][key] = data[section][key]
	
	with open(inifile, 'w') as f:
		config.write(f)


def get_args():

    parser = argparse.ArgumentParser()

    parser.add_argument('-agent', type=str, help='Set the agent name', required=True)

    parser.add_argument('-location', type=str, help='Set the agent Geo location (i.e City name)', required=True)

    parser.add_argument('-cloud', type=str, help='Set the cloud name that host the agent (i.e AWS, GCE, or other 3rd party provider)', required=True)

    parser.add_argument('-zone', type=str, help='Set the cloud Geo location (i.e us-east-1)', required=True)

    parser.add_argument('-hidden', type=str, help='hide agent from the drop list location in UI (1=hide, 0=unhide)', required=True)    

    parser.add_argument('-inifile', type=str, help='Set locations.ini config file', required=True)

    return parser.parse_args()


def main():

	args = get_args()

	config = configparser.ConfigParser()

	config.read(args.inifile)

	if not args.location in config:

		agent_data = {args.location: {"label": '"' + args.location + '"', "1": args.agent, "hidden": args.hidden}, args.agent: {"label": ' '.join([args.cloud, args.zone]) + ': Support Chrome,Firefox',"browser": "Chrome,Firefox"}}

		create_location(config, args.location, agent_data, args.inifile)
	else:
		print(' '.join([args.agent, "agent in location", args.location, "already configured in the system"]))


if __name__ == '__main__':
	main()
