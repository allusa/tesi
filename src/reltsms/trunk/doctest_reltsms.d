
//docstest reltsms
BEGIN;
VAR reltsmsdoctest BOOLEAN INIT (true);



//ts.t
reltsmsdoctest := 
WITH RELATION {
 TUPLE { t 2.0, v 3.0 }
 } AS m1: 
reltsmsdoctest and ts.t(m1) = 2.0;

//ts.v
reltsmsdoctest := 
WITH RELATION {
 TUPLE { t 2.0, v 3.0 }
 } AS m1: 
reltsmsdoctest and ts.v(m1) = 3.0;


//ts.union
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
   TUPLE { t 5.0, v 3.0 },
   TUPLE { t 6.0, v 4.0 },
   TUPLE { t 10.0, v 1.0 }
  } AS tsr
: 
reltsmsdoctest and ts.union(ts1,ts2) = tsr;



output reltsmsdoctest;
END;
