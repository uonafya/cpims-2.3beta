/* Uncomment if it fails running indication the sequence does not exist */
/* create sequence public.ovc_monitoring_monitoring_id_seq
  owned by ovc_monitoring.monitoring_id; */

alter table ovc_monitoring alter column monitoring_id set default nextval('public.ovc_monitoring_monitoring_id_seq'::regclass);

/* Set value of sequence to last value in table in the case that it is not set */
/*
SELECT setval('ovc_monitoring_monitoring_id_seq', 100, true);
 */