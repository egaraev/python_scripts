#!/usr/bin/env bash

dateFull=$(date '+%Y-%m-%d_%H-%M-%S')


if [ $# -eq 0 ]; then
  echo "Usage: $0 [-i|--instance] [-h|--backup-host]"
  exit 1
fi

for i in "$@"; do
  echo $i
  case $i in
    -i=*|--instance=*)
      INSTANCE="${i#*=}"
      shift
      ;;
    -h=*|--backup-host=*)
      BACKUP_HOST="${i#*=}"
      shift
      ;;
    -h|--help)
      echo "Usage: $0 [-i|--instance] [-h|--backup-host]"
      exit 1
      ;;
    *)
      echo "Usage: $0 [-i|--instance] [-h|--backup-host]"
      exit 1
      ;;
  esac
done

echo "Backup  database"

ansible $BACKUP_HOST -a "/home/rsync/rsync_backup.sh" --become --become-user rsync

echo "Backup completed"