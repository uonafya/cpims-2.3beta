#!/bin/bash

psql -h $1  -U $2 -d $3 -o $4 -c 'select ovc_registration_id, age, first_name from data_quality_view'