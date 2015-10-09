
//docstest reltsms
BEGIN;
VAR reltsmsdoctest BOOLEAN INIT (true);





//multivalued2canonical
reltsmsdoctest :=
WITH RELATION {
 TUPLE { t 1.0, v1 4.0, v2 5.0 },
 TUPLE { t 2.0, v1 5.0, v2 5.0 }
 } AS smv,
RELATION {
 TUPLE { t 1.0, v relation { tuple {v1 4.0, v2 5.0 }} },
 TUPLE { t 2.0, v relation { tuple {v1 5.0, v2 5.0 }} }
 } AS sc:
reltsmsdoctest and smv group ({all but t} as v) = sc;

//canonical2multivalued
reltsmsdoctest :=
WITH RELATION {
 TUPLE { t 1.0, v1 4.0, v2 5.0 },
 TUPLE { t 2.0, v1 5.0, v2 5.0 }
 } AS smv,
RELATION {
 TUPLE { t 1.0, v relation { tuple {v1 4.0, v2 5.0 }} },
 TUPLE { t 2.0, v relation { tuple {v1 5.0, v2 5.0 }} }
 } AS sc:
reltsmsdoctest and sc ungroup (v) = smv;





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




output reltsmsdoctest;
END;
