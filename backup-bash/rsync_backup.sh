#!/bin/bash

set -o errexit
set -o pipefail

# set up few variables connected with date for convenience
dateWithHour=$(date '+%Y-%m-%d_%H')
dateFull=$(date '+%Y-%m-%d_%H-%M-%S')
date=$(date '+%Y-%m-%d')
year=$(date '+%Y')
month=$(date '+%B')
week=$((($(date +%-d)-1)/7+1))
day=$(date '+%d')


# set up path for backup  files
backupPath=/data/backup_storage # directory for all backup related operations
SourceDataPath=/data/db   # default source path to  database files

# variables with remote username and remote host for backup
remoteUser="rsync"
remoteHost=192.168.0.100

archive=false
short_archive=false

IGNOREEXIT=24
IGNOREOUT='^(file has vanished: |rsync warning: some files vanished before they could be transferred)'

for i in "$@"; do
   case "$@" in
      "")
         shift
         ;;
      --help|-h)
         echo "Usage: $0 [-a|--archive] [-s|--short]"
         exit 1
         ;;
      --archive|-a)
         archive=true
         shift
         ;;
      --short|-s)
         short_archive=true
         archive=true
         shift
         ;;
   esac
done

echo "Starting backup on $(date) $remoteUser@$remoteHost from path $SourceDataPath"

#make sub directories
mkdir -p $backupPath/archive
mkdir -p $backupPath/db

#sync database files
set +e
rsync -e "ssh -o StrictHostKeyChecking=no" -avzHAX --delete --numeric-ids --rsync-path='sudo rsync' "$remoteUser@$remoteHost:$SourceDataPath" $backupPath/db | (egrep -v "$IGNOREOUT" || true)
result=$?
if [[ $result == $IGNOREEXIT ]]; then
    result=0
fi
set -e

if [[ $result != 0 ]]; then
  echo "rsync failure"
  exit 1
fi

echo $archive

if [ "$archive" = true ] && [ "$short_archive" = false ]; then
    echo "Archive mode"

    mkdir -p $backupPath/archive/monthly_bckp
    mkdir -p $backupPath/archive/weekly_bckp
    mkdir -p $backupPath/archive/daily_bckp
    mkdir -p $backupPath/archive/hourly_bckp
    
    which=$(date '+%-H')

    if [[ $(($which)) -lt 8 ]] || [[ $(($which)) -gt 18 ]]; then
      if [[ $((which%2)) -eq 0 ]]; then
        tar -zcvf "$backupPath/archive/hourly_bckp/backup_$dateWithHour.tar.gz" -C $backupPath/db .
      fi
    else
      tar -zcvf "$backupPath/archive/hourly_bckp/backup_$dateWithHour.tar.gz" -C $backupPath/db .
    fi 
    if [[ $(($which)) -eq 23 ]]; then
      tar -zcvf "$backupPath/archive/daily_bckp/backup-$date.tar.gz" -C $backupPath/db .

      #archive on end of week
      weekEndCheck=$((($(date +%-d -d "1hour")-1)/7+1))
      if [[ $weekEndCheck -ne week ]]; then
        cp "$backupPath/archive/daily_bckp/backup-$date.tar.gz" "$backupPath/archive/weekly_bckp/backup-$year-$month-week_$week.tar.gz"
      fi

      #archive on end of month
      today=$(date +%d)
      tomorrow=$(date +%-d -d "1day")
      if [[ $tomorrow -lt $today ]]; then
        cp "$backupPath/archive/daily_bckp/backup-$date.tar.gz" "$backupPath/archive/monthly_bckp/backup-$year-$month.tar.gz"
      fi
    fi

    if [[ $(ls -1 $backupPath/archive/hourly_bckp | wc -l) -gt 17 ]]; then
      rm $(ls -tp $backupPath/archive/hourly_bckp/* | tail -n 1)
    fi

    if [[ $(ls -1 $backupPath/archive/daily_bckp | wc -l) -gt 7 ]]; then
      rm $(ls -tp $backupPath/archive/daily_bckp/* | tail -n 1)
    fi

    if [[ $(ls -1 $backupPath/archive/weekly_bckp | wc -l) -gt 5 ]]; then
      rm $(ls -tp $backupPath/archive/weekly_bckp/* | tail -n 1)
    fi

    if [[ $(ls -1 $backupPath/archive/monthly_bckp | wc -l) -gt 6 ]]; then
      rm $(ls -tp $backupPath/archive/monthly_bckp/* | tail -n 1)
    fi
elif [ "$archive" = true ] && [ "$short_archive" = true ]; then
    echo "Short archive mode"

    mkdir -p $backupPath/archive/daily_bckp
    mkdir -p $backupPath/archive/hourly_bckp

    tar -zcvf "$backupPath/archive/hourly_bckp/backup_$dateWithHour.tar.gz" -C $backupPath/db .

    if [[ $(ls -1 $backupPath/archive/hourly_bckp | wc -l) -gt 4 ]]; then
      yesterday=$(date '+%Y-%m-%d' -d "-1day")
      if [ ! -f $backupPath/archive/daily_bckp/backup-$yesterday.tar.gz ]; then
        cp $(ls -tp $backupPath/archive/hourly_bckp/* | tail -n 1) $backupPath/archive/daily_bckp/backup-$yesterday.tar.gz
      fi

      rm $(ls -tp $backupPath/archive/hourly_bckp/* | tail -n 1)
    fi

    if [[ $(ls -1 $backupPath/archive/daily_bckp | wc -l) -gt 4 ]]; then
      rm $(ls -tp $backupPath/archive/daily_bckp/* | tail -n 1)
    fi
else
    echo "Manual backup"
    mkdir -p $backupPath/archive/manual_bckp
    tar -zcvf "$backupPath/archive/manual_bckp/backup_$dateFull.tar.gz" -C $backupPath/db .
    if [[ $(ls -1 $backupPath/archive/manual_bckp | wc -l) -gt 10 ]]; then
      rm $(ls -tp $backupPath/archive/manual_bckp/* | tail -n 1)
    fi
    echo "Backup from $remoteHost saved to $backupPath/archive/manual_bckp/backup_$dateFull.tar.gz"
fi

echo "Backup end - $(date)"
