CREATE OR REPLACE FUNCTION FN_HHVA_MAIN ()
  RETURNS character varying AS $output$
DECLARE
   RESULT ovc_care_events%rowtype;
   OUTPUT INTEGER;
   SQL_DROP_TABLE VARCHAR(100);
   SQL_CREATE_TABLE VARCHAR(1000);	
   
BEGIN
   SQL_DROP_TABLE = 'DROP TABLE IF EXISTS temp_hhva_ranking';
   SQL_CREATE_TABLE = 'CREATE TABLE temp_hhva_ranking(event uuid, event_type_id varchar(20), person_id int, house_hold_id uuid, entity varchar(20), value varchar(20))';
   EXECUTE SQL_DROP_TABLE;
   EXECUTE SQL_CREATE_TABLE;
   
   FOR RESULT IN
      SELECT * FROM ovc_care_events WHERE house_hold_id IS NOT NULL
   LOOP  
	RAISE NOTICE 'VALUE: %', RESULT.house_hold_id;	
	EXECUTE ('INSERT INTO temp_hhva_ranking(event, event_type_id, person_id, house_hold_id, entity, value) 
		SELECT event, event_type_id, person_id, house_hold_id, entity, value FROM ovc_care_events 
		INNER JOIN ovc_care_eav ON ovc_care_events.event=ovc_care_eav.event_id 
		WHERE ovc_care_events.event_type_id=''FHSA'' AND ovc_care_events.house_hold_id=''' || RESULT.house_hold_id || ''''); 
	
   END LOOP;
   RETURN OUTPUT;
END
$output$  LANGUAGE plpgsql


SELECT FN_HHVA_MAIN()