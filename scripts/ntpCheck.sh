#!/bin/bash
#
# h/t https://github.com/cadusilva
#

# Check if argument is passed
if [ -z "$1" ]; then
  echo "Usage: $0 <NTP_SERVER>"
  exit 1
fi

# Assign the argument to a variable
NTP_SERVER=$1

# Only allow DNS names or IP literals; the value is embedded in a chronyd directive
if ! [[ $NTP_SERVER =~ ^[A-Za-z0-9_.:-]{1,253}$ ]]; then
  echo "Invalid server name: $NTP_SERVER" >&2
  exit 1
fi

chronyd -Q -t 5 "server $NTP_SERVER iburst maxsamples 1"
