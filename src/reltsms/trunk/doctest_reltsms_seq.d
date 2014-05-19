
//docstest reltsms
BEGIN;
VAR reltsmsdoctest BOOLEAN INIT (true);



//interval

reltsmsdoctest := 
WITH 
 RELATION {
   TUPLE { t 2.0, v 3.0 },
   TUPLE { t 4.0, v 2.0 },
   TUPLE { t 6.0, v 3.0 }
  } AS ts1:
reltsmsdoctest and ts.interval.closed(ts1,2.0,6.0) = ts1;

reltsmsdoctest := 
WITH 
 RELATION {
   TUPLE { t 2.0, v 3.0 },
   TUPLE { t 4.0, v 2.0 },
   TUPLE { t 6.0, v 3.0 }
  } AS ts1,
 RELATION {
   TUPLE { t 4.0, v 2.0 },
   TUPLE { t 6.0, v 3.0 }
  } AS r:
reltsmsdoctest and ts.interval.left(ts1,2.0,6.0) = r;





output reltsmsdoctest;
END;
