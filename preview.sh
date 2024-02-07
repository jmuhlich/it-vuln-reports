#!/bin/bash

python tenable_convert.py "$@" \
    | xsv select 'DNS Name,IP Address,Path' \
    | xsv sort \
    | xsv table
