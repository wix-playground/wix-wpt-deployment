#! /bin/bash

# kill wix-wpt process which greater then 900 sec
kill -9 $(ps -eo user,pid,etimes,cmd | grep wix-wpt | grep -v grep | awk '{if ($3 > 900) { print $2}}')