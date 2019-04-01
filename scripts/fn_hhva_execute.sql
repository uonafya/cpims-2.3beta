CREATE OR REPLACE FUNCTION FN_HHVA_EXECUTE ()
  RETURNS character varying AS $output$
DECLARE
   OUTPUT INTEGER; 
   SQL_DROP_TABLE VARCHAR(100);  
BEGIN

	UPDATE ovc_care_events SET event_score=i.event_score FROM (SELECT house_hold_id,
	CASE WHEN SUM(vulnerability)=0 THEN 'NOT RANKED'
		WHEN SUM(vulnerability) BETWEEN 1 AND 9 THEN 'LOWER'
		WHEN SUM(vulnerability) BETWEEN 10 AND 18 THEN 'MEDIUM'
		WHEN SUM(vulnerability) >=19 THEN 'HIGH'
		END
	AS hhva_score,
	CASE WHEN SUM(vulnerability)=0 THEN 0
		WHEN SUM(vulnerability) BETWEEN 1 AND 9 THEN 1
		WHEN SUM(vulnerability) BETWEEN 10 AND 18 THEN 2
		WHEN SUM(vulnerability) >=19 THEN 3
		END
	AS event_score
	FROM(

	SELECT house_hold_id, 
	CASE 
		-- HA5
		WHEN entity='HA5'AND value='HAPT' THEN 1
		WHEN entity='HA5'AND value='HAPP' THEN 1
		WHEN entity='HA5'AND value='HARC' THEN 1
		WHEN entity='HA5'AND value='HA5D' THEN 1
		WHEN entity='HA5'AND value='HA5B' THEN 1
		WHEN entity='HA5'AND value='HA5L' THEN 1
		WHEN entity='HA5'AND value='HA5P' THEN 1
		WHEN entity='HA5'AND value='HA5P' THEN 1
		WHEN entity='HA5'AND value='HA5S' THEN 1
		WHEN entity='HA5'AND value='HA5R' THEN 1

		-- HA7
		WHEN entity='HA7'AND value='HAOD' THEN 1
		WHEN entity='HA7'AND value='HARP' THEN 1
		WHEN entity='HA7'AND value='HAFT' THEN 1
		WHEN entity='HA7'AND value='HAPL' THEN 1

		-- HA11
		WHEN entity='HA11'AND value='HA1D' THEN 1
		WHEN entity='HA11'AND value='HA2D' THEN 1
		WHEN entity='HA11'AND value='HA3D' THEN 1

		-- HA12
		WHEN entity='HA12'AND value='HADN' THEN 1
		WHEN entity='HA12'AND value='HALS' THEN 1
		WHEN entity='HA12'AND value='HAMP' THEN 1
		WHEN entity='HA12'AND value='HAOF' THEN 1

		-- HA13
		WHEN entity='HA13'AND value='HIFE' THEN 1
		WHEN entity='HA13'AND value='HISB' THEN 1
		WHEN entity='HA13'AND value='HICL' THEN 1
		WHEN entity='HA13'AND value='HIBK' THEN 1
		WHEN entity='HA13'AND value='HIDD' THEN 1
		WHEN entity='HA13'AND value='HICT' THEN 1
		WHEN entity='HA13'AND value='HIBB' THEN 1
		WHEN entity='HA13'AND value='HIFF' THEN 1
		WHEN entity='HA13'AND value='HILR' THEN 1
		WHEN entity='HA13'AND value='HICF' THEN 1

		-- HA14
		WHEN entity='HA14'AND value='HIFM' THEN 1
		WHEN entity='HA14'AND value='HILR' THEN 1
		WHEN entity='HA14'AND value='HISO' THEN 1

		-- HA16
		WHEN entity='HA16'AND value='HIGA' THEN 1
		WHEN entity='HA16'AND value='HICO' THEN 1
		WHEN entity='HA16'AND value='HIPF' THEN 1
		WHEN entity='HA16'AND value='HIFW' THEN 1

		-- HA19
		WHEN entity='HA19'AND value='HITF' THEN 1
		WHEN entity='HA19'AND value='HIET' THEN 1
		WHEN entity='HA19'AND value='HISF' THEN 1
		WHEN entity='HA19'AND value='HIMB' THEN 1
		WHEN entity='HA19'AND value='HICL' THEN 1
		WHEN entity='HA19'AND value='HIRN' THEN 1
		WHEN entity='HA19'AND value='HIFD' THEN 1

		-- ELSE
		ELSE 0 
	END AS vulnerability
	FROM temp_hhva_ranking

	) AS hhva_assessment
	GROUP BY house_hold_id) i
	WHERE i.house_hold_id=ovc_care_events.house_hold_id;

   SQL_DROP_TABLE = 'DROP TABLE IF EXISTS temp_hhva_ranking';
   EXECUTE SQL_DROP_TABLE;   
   RETURN OUTPUT;
END
$output$  LANGUAGE plpgsql