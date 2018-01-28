#!/bin/bash

awk '$9~/404|^30/' ~/Downloads/NASA_access_log_Jul95 | awk '{print "HTTP error: " $9 "\t" $7}' | sort | uniq 

#> ~/Downloads/nasa-broken-relocated-urls