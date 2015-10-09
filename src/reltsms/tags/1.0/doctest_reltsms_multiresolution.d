
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


reltsmsdoctest := 
WITH 
 RELATION {
   TUPLE { t 4.0, v 1.0},
   TUPLE { t 5.0, v 6.0 },
   TUPLE { t 8.0, v 2.0 }
  } AS ts1,
 RELATION {
   TUPLE { t -5.0, v 1.0 },
   TUPLE { t 5.0, v 6.0 }
  } AS tsr:
reltsmsdoctest and mtsms.dmap(ts1,10.0,-5.0,'mtsms.aaf.maxzohe',3.0) = tsr;



//multiresolution
reltsmsdoctest := 
WITH 
 RELATION {
   TUPLE { t 4.0, v 1.0},
   TUPLE { t 5.0, v 6.0 },
   TUPLE { t 8.0, v 2.0 }
  } AS ts1,
 RELATION {
   TUPLE { delta 2.0, tau 0.0, f 'mtsms.aaf.maxzohe', k 4.0},
   TUPLE { delta 5.0, tau 0.0, f 'mtsms.aaf.maxzohe', k 2.0}
  } AS schema,
 RELATION {
   TUPLE { t 0.0, v 1.0 },
   TUPLE { t 2.0, v 1.0 },
   TUPLE { t 4.0, v 1.0 },
   TUPLE { t 6.0, v 6.0 },
   TUPLE { t 8.0, v 2.0 }
  } AS tsr:
reltsmsdoctest and mtsms.multiresolution(ts1,schema) = tsr;

reltsmsdoctest := 
WITH 
 RELATION {
   TUPLE { t 4.0, v 1.0},
   TUPLE { t 5.0, v 6.0 },
   TUPLE { t 8.0, v 2.0 }
  } AS ts1,
 RELATION {
   TUPLE { delta 5.0, tau 2.0, f 'mtsms.aaf.maxzohe', k 2.0},
   TUPLE { delta 10.0, tau -10.0, f 'mtsms.aaf.maxzohe', k 3.0}
  } AS schema,
 RELATION {
   TUPLE { t -10.0, v 1.0 },
   TUPLE { t 0.0, v 1.0 },
   TUPLE { t 2.0, v 1.0 },
   TUPLE { t 7.0, v 6.0 }
  } AS tsr:
reltsmsdoctest and mtsms.multiresolution(ts1,schema) = tsr;



output reltsmsdoctest;
END;
