#! /bin/bash

WORKS='/var/www/webpagetest/www/work/jobs'

for agent_works in $(ls $WORKS)
  do
	find $WORKS/$agent_works -type f -cmin +29 -name "*.*" -exec sudo rm -f {} \;
done
