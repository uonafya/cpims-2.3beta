#!/bin/bash
psql -h $1  -U $2 -d $3 -o $4 -c 'select first_name,other_names, surname, sex_id, school_level, designation, is_disabled,has_bcert, age, hiv_status, art_status from data_quality_view'
