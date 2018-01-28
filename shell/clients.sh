#!/bin/bash

cat ~/Downloads/NASA_access_log_Jul95 | grep ".html" | awk '{print $1}' | sort | uniq -ic | sort -n -r | awk '{print $2 "\t" $1}' 

#> ~/Downloads/sorted.txt