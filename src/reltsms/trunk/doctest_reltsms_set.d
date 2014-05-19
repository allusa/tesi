
//docstest reltsms
BEGIN;
VAR reltsmsdoctest BOOLEAN INIT (true);


//ts.max
reltsmsdoctest := 
WITH 
 RELATION {
   TUPLE { t 2.0, v 3.0 },
   TUPLE { t 4.0, v 2.0 },
   TUPLE { t 6.0, v 4.0 }
  } AS ts1,
 RELATION {
   TUPLE { t 6.0, v 4.0 }
  } AS tsr:
reltsmsdoctest and ts.max(ts1) = tsr;

//ts.min
reltsmsdoctest := 
WITH 
 RELATION {
   TUPLE { t 2.0, v 3.0 },
   TUPLE { t 4.0, v 2.0 },
   TUPLE { t 6.0, v 4.0 }
  } AS ts1,
 RELATION {
   TUPLE { t 2.0, v 3.0 }
  } AS tsr:
reltsmsdoctest and ts.min(ts1) = tsr;


//ts.sup
reltsmsdoctest := 
WITH 
 RELATION {
   TUPLE { t 2.0, v 3.0 },
   TUPLE { t 4.0, v 2.0 },
   TUPLE { t 6.0, v 4.0 }
  } AS ts1:
reltsmsdoctest and ts.sup(ts1) = ts.max(ts1);

reltsmsdoctest := 
WITH 
 RELATION {t rational, v rational}
 {	  
  } AS ts1,
 RELATION {
   TUPLE { t -1.0/0.0, v 1.0/0.0 }
  } AS tsr:
reltsmsdoctest and ts.sup(ts1) = tsr;

//ts.inf
reltsmsdoctest := 
WITH 
 RELATION {
   TUPLE { t 2.0, v 3.0 },
   TUPLE { t 4.0, v 2.0 },
   TUPLE { t 6.0, v 4.0 }
  } AS ts1:
reltsmsdoctest and ts.inf(ts1) = ts.min(ts1);

reltsmsdoctest := 
WITH 
 RELATION {t rational, v rational}
 {	  
  } AS ts1,
 RELATION {
   TUPLE { t 1.0/0.0, v 1.0/0.0 }
  } AS tsr:
reltsmsdoctest and ts.inf(ts1) = tsr;




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


//ts.union.t
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
   TUPLE { t 10.0, v 1.0 }
  } AS tsr
: 
reltsmsdoctest and ts.union.t(ts1,ts2) = tsr;






//projection 
reltsmsdoctest := 
WITH 
 RELATION {
   TUPLE { t 2.0, v 3.0 },
   TUPLE { t 4.0, v 2.0 },
   TUPLE { t 6.0, v 4.0 }
  } AS ts1,
 RELATION {
   TUPLE { t 2.0 },
   TUPLE { t 4.0 },
   TUPLE { t 6.0 }
  } AS r: 
reltsmsdoctest and ts1 {t} = r;

reltsmsdoctest := 
WITH 
 RELATION {
   TUPLE { t 2.0, v 3.0 },
   TUPLE { t 4.0, v 2.0 },
   TUPLE { t 6.0, v 3.0 }
  } AS ts1,
 RELATION {
   TUPLE { v 2.0 },
   TUPLE { v 3.0 }
  } AS r: 
reltsmsdoctest and ts1 {v} = r;



//selection-restriction
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
reltsmsdoctest and (ts1 where t>2.0) = r;


//rename
reltsmsdoctest := 
WITH 
 RELATION {
   TUPLE { t 2.0, v 3.0 },
   TUPLE { t 4.0, v 2.0 },
   TUPLE { t 6.0, v 3.0 }
  } AS ts1,
 RELATION {
   TUPLE { t 2.0, temp 3.0 },
   TUPLE { t 4.0, temp 2.0 },
   TUPLE { t 6.0, temp 3.0 }
  } AS r:
reltsmsdoctest and ts1 rename (v as temp) = r;




output reltsmsdoctest;
END;
