#!/bin/bash
# This script checks if a process with a given keyword is running. If not, it executes a given command to start the process.
# Usage [In crontab -e] * * * * * <Absolute path>/keepAppRun.sh <keyword which is checked in ps aux> <command to start the process>
# Example:
# * * * * * /root/0_GIT_WSN_SERVER_CLUSTER/0_SHARE/keepAppRun.sh "myapp" "python3 myapp.py"
# * * * * * /root/0_GIT_WSN_SERVER_CLUSTER/0_SHARE/keepAppRun.sh "sleep.sh" 'sh /root/0_GIT_WSN_SERVER_CLUSTER/0_SHARE/sleep.sh'

DEBUG_LOG_FLAG=1 # 0: Disable, 1: Enable
#NOTE: Print log to console and log file at: /KeepAppRun_xxx.log

#Create log file name
if [ "$#" -gt 1 ]; then
  keyWordInput="$1"
  LOG_FILE=$(echo "KeepAppRun_$keyWordInput" | sed -e 's/[ \/\\]/_/g' | sed -e 's/[^A-Za-z0-9_.-]//g')
else
  LOG_FILE="KeepAppRun_NoArgs"
fi
LOG_FILE="/$LOG_FILE.log"

if [ "$DEBUG_LOG_FLAG" -eq 1 ]; then
  echo -e "\x1b[38;5;2m=== Check Run App Log: $(date) ===\x1b[0m" | tee "$LOG_FILE"
  # Print all arguments to the log file
  echo -e "\x1b[38;5;2mArgument number: $#\x1b[0m" | tee -a "$LOG_FILE"
  i=0
  while [ "$i" -lt "$#" ]; do
    echo -e "\x1b[38;5;2mArgument $i: ${!i}\x1b[0m" | tee -a "$LOG_FILE"
    i=$((i+1))
  done

  echo "" | tee -a "$LOG_FILE"
fi

if [ "$#" -gt 1 ]; then
  checkKeyWord="$1"
  shOpenApp="$2"
  numCnt=$(ps aux | grep -v grep | grep -vi keepAppRun | grep "$checkKeyWord" | wc -l)

  if [ "$DEBUG_LOG_FLAG" -eq 1 ]; then
    # Print Found keyword number
    echo -e "\x1b[38;5;3mFound ($numCnt) keyword: $checkKeyWord\x1b[0m" | tee -a "$LOG_FILE"
    ps aux | grep -v grep | grep -vi keepAppRun | grep "$checkKeyWord" | tee -a "$LOG_FILE"
  fi

  if [ "$numCnt" -lt 1 ]; then
    if [ "$DEBUG_LOG_FLAG" -eq 1 ]; then
      echo -e "\x1b[38;5;3mCheck: $checkKeyWord is not running\x1b[0m" | tee -a "$LOG_FILE"
      echo -e "\x1b[38;5;3mExec: $shOpenApp\x1b[0m" | tee -a "$LOG_FILE"
    fi
    eval "$shOpenApp"
  fi
else
  if [ "$DEBUG_LOG_FLAG" -eq 1 ]; then
    echo -e "\x1b[38;5;1mError: Not enough arguments\x1b[0m" | tee -a "$LOG_FILE"
  fi
fi
