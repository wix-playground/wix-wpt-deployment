#! /bin/bash

RESULTS='/var/www/webpagetest/www/results'

PREV_YEAR_MONTH=$(date --date='-1 month' +%y/%m)

CURR_YEAR_MONTH=$(date +%y/%m)

if [ -d $RESULTS/$PREV_YEAR_MONTH ]
  then
	sudo rm -rf $RESULTS/$PREV_YEAR_MONTH
fi

find $RESULTS/$CURR_YEAR_MONTH -maxdepth 1 -type d -ctime +7 -exec sudo rm -rf {} \;
