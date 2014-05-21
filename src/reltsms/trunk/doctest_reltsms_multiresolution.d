
//multiresolution over TSMS
BEGIN;
VAR reltsmsdoctest BOOLEAN INIT (true);


//maxzohe
reltsmsdoctest := 
WITH 
 RELATION {
   TUPLE { t 2.0, v 3.0 },
   TUPLE { t 4.0, v 2.0 },
   TUPLE { t 6.0, v 4.0 }
  } AS ts1,
 RELATION {
   TUPLE { t 5.0, v 4.0 }
  } AS tsr:
reltsmsdoctest and mtsms.aaf.maxzohe(ts1,2.0,5.0) = tsr;


//dmap
reltsmsdoctest := 
WITH 
 RELATION {
   TUPLE { t 4.0, v 1.0},
   TUPLE { t 5.0, v 6.0 },
   TUPLE { t 8.0, v 2.0 }
  } AS ts1,
 RELATION {
   TUPLE { t 2.0, v 1.0 },
   TUPLE { t 4.0, v 1.0 },
   TUPLE { t 6.0, v 6.0 },
   TUPLE { t 8.0, v 2.0 }
  } AS tsr:
reltsmsdoctest and mtsms.dmap(ts1,2.0,0.0,'mtsms.aaf.maxzohe',4.0) = tsr;


reltsmsdoctest := 
WITH 
 RELATION {
   TUPLE { t 4.0, v 1.0},
   TUPLE { t 5.0, v 6.0 },
   TUPLE { t 7.0, v 2.0 }
  } AS ts1,
 RELATION {
   TUPLE { t 0.0, v 1.0 },
   TUPLE { t 2.0, v 1.0 },
   TUPLE { t 4.0, v 1.0 },
   TUPLE { t 6.0, v 6.0 }
  } AS tsr:
reltsmsdoctest and mtsms.dmap(ts1,2.0,0.0,'mtsms.aaf.maxzohe',4.0) = tsr;



output reltsmsdoctest;
END;
