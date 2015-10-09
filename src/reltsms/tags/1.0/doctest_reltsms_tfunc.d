
//docstest reltsms
BEGIN;
VAR reltsmsdoctest BOOLEAN INIT (true);



//zohe temporal interval

reltsmsdoctest := 
WITH 
 RELATION {
   TUPLE { t 2.0, v 3.0 },
   TUPLE { t 4.0, v 2.0 },
   TUPLE { t 6.0, v 3.0 }
  } AS ts1:
reltsmsdoctest and ts.interval.zohe(ts1,1.0,6.0) = ts1;

reltsmsdoctest := 
WITH 
 RELATION {
   TUPLE { t 2.0, v 3.0 },
   TUPLE { t 4.0, v 2.0 },
   TUPLE { t 6.0, v 3.0 }
  } AS ts1,
 RELATION {
   TUPLE { t 4.0, v 2.0 },
   TUPLE { t 5.0, v 3.0 }
  } AS tsr:
reltsmsdoctest and ts.interval.zohe(ts1,2.0,5.0) = tsr;

reltsmsdoctest := 
WITH 
 RELATION {
   TUPLE { t 2.0, v 3.0 },
   TUPLE { t 4.0, v 2.0 },
   TUPLE { t 6.0, v 3.0 }
  } AS ts1,
 RELATION {
   TUPLE { t 4.0, v 2.0 },
   TUPLE { t 6.0, v 3.0 },
   TUPLE { t 7.0, v 1.0/0.0 }
  } AS tsr:
reltsmsdoctest and ts.interval.zohe(ts1,2.0,7.0) = tsr;




//ts.concatenation
reltsmsdoctest := 
WITH 
 RELATION {
   TUPLE { t 2.0, v 3.0 },
   TUPLE { t 4.0, v 2.0 },
   TUPLE { t 6.0, v 4.0 }
  } AS ts1,
 RELATION {
   TUPLE { t 1.0, v 2.0 },
   TUPLE { t 5.0, v 3.0 },
   TUPLE { t 6.0, v 5.0 },
   TUPLE { t 10.0, v 1.0 }
  } AS ts2,
 RELATION {
   TUPLE { t 1.0, v 2.0 },
   TUPLE { t 2.0, v 3.0 },
   TUPLE { t 4.0, v 2.0 },
   TUPLE { t 6.0, v 4.0 },
   TUPLE { t 10.0, v 1.0 }
  } AS tsr
: 
reltsmsdoctest and ts.concatenation.t(ts1,ts2,'zohe') = tsr;




output reltsmsdoctest;
END;
