#!/bin/bash
# wait-for-postgres.sh

set -e

host="$1"
port="$2"
shift 2
cmd="$@"

until PGPASSWORD=$POSTGRES_PASSWORD pg_isready -h "$host" -p "$port" > /dev/null 2>&1; do
  >&2 echo "PostgreSQL is unavailable - sleeping..."
  sleep 1
done

>&2 echo "PostgreSQL is ready on $host:$port - executing command"
exec $cmd
