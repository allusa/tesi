
BEGIN;


WITH 
 RELATION {
   TUPLE { delta 1296000.0, tau 1302480000.0, f 'mtsms.aaf.maxzohe', k 12.0},
   TUPLE { delta 4320000.0, tau 1266624000.0, f 'mtsms.aaf.maxzohe', k 12.0}
  } AS schema:
mtsms.multiresolution(ts1,schema)


END;