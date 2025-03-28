#!/usr/bin/env bash

# wait-for-it.sh host:port [-s] [-t timeout] [-- command args]
# -h HOST | --host=HOST       Host or IP under test
# -p PORT | --port=PORT       TCP port under test
#                           Alternatively, you specify the host and port as host:port
# -s | --strict               Only execute subcommand if the test succeeds
# -q | --quiet                Don't output any status messages
# -t TIMEOUT | --timeout=TIMEOUT
#                           Timeout in seconds, zero for no timeout
# -- COMMAND ARGS             Execute command with args after the test finishes

TIMEOUT=15
STRICT=false
QUIET=false

while getopts "h:p:t:sq" opt; do
  case $opt in
    h)
      HOST=$OPTARG
      ;;
    p)
      PORT=$OPTARG
      ;;
    t)
      TIMEOUT=$OPTARG
      ;;
    s)
      STRICT=true
      ;;
    q)
      QUIET=true
      ;;
    *)
      echo "Usage: $0 -h host -p port [-t timeout] [-s] [-q] -- command"
      exit 1
      ;;
  esac
done
shift $((OPTIND - 1))

if [ -z "$HOST" ] || [ -z "$PORT" ]; then
  echo "Usage: $0 -h host -p port [-t timeout] [-s] [-q] -- command"
  exit 1
fi

# Wait for the host and port
for i in $(seq 1 $TIMEOUT); do
  nc -z $HOST $PORT > /dev/null 2>&1
  result=$?
  
  if [ $result -eq 0 ]; then
    if [ "$QUIET" = false ]; then
      echo "$HOST:$PORT is available"
    fi
    break
  fi
  
  if [ $i -eq $TIMEOUT ]; then
    if [ "$STRICT" = true ]; then
      echo "$HOST:$PORT is still not available after $TIMEOUT seconds"
      exit 1
    fi
    if [ "$QUIET" = false ]; then
      echo "$HOST:$PORT not available, waiting..."
    fi
  fi
  
  sleep 1
done

# Execute the command
if [ $# -gt 0 ]; then
  exec "$@"
fi
