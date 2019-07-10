#!/bin/bash
psql -h $1  -U $2 -d $3 -o $4 -c 'select first_name, age, hiv_status, art_status from data_quality_view'
