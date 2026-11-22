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

# chronyd is often in an sbin directory that is not on a regular user's PATH
CHRONYD=$(command -v chronyd)
if [ -z "$CHRONYD" ]; then
  for dir in /usr/sbin /usr/local/sbin /opt/homebrew/sbin /opt/homebrew/bin /usr/local/bin /usr/bin /sbin; do
    if [ -x "$dir/chronyd" ]; then
      CHRONYD="$dir/chronyd"
      break
    fi
  done
fi
if [ -z "$CHRONYD" ]; then
  echo "chronyd not found" >&2
  exit 1
fi

"$CHRONYD" -Q -t 5 "server $NTP_SERVER iburst maxsamples 1"
