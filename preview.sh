#!/bin/bash

set -euo pipefail

base=$(dirname "$0")

python "$base"/tenable_convert.py "$@" \
    | xsv select 'DNS Name,IP Address,Location,FixedVersion,Plugins' \
    | xsv sort \
    | xsv table
