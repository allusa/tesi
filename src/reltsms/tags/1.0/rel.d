





//type prova2 POSSREP a {qty integer} POSSREP b {qtyf rational} INIT a (qtyf:=CAST_AS_RATIONAL(qty)) b (qty:=2);

//type provats POSSREP { ts same_type_as(timeseries) };

//provats(relation { tuple{t 1.0, v 2.0} })

//with provats(relation { tuple{t 1.0, v 2.0} }) as st:
//THE_ts(st)

//type provats2 POSSREP ts {ts relation t,v} POSSREP ts2 {ts2 relation t,v1,v2} INIT ts (ts2:=) b (qty:=2);

// multivalued2canonical -> potser es pot fer amb grup/ungroup o wrap/unwrap ?
//extend r add ( (r rename (t as tr) where t=tr) {ALL BUT tr} as vr ) {t,vr} rename (vr as v)
//multivalued2canonical
//r group ({all but t} as v)
//canonical2multivalued
// ungroup (v)



//MULTIVALUED to CANONICAL
//OPERATOR ts.canonical(s1 RELATION {}) RETURNS RELATION SAME_HEADING_AS  (timeseries);
//return extend s1 add ( WITH t as t1: (s1 where t=t1) {ALL BUT t} as v) {t,v};
//END OPERATOR;

//WITH RELATION {
//TUPLE { t 1.0, v1 4.0, v2 5.0 },
//TUPLE { t 2.0, v1 5.0, v2 5.0 }
// } AS s1:
// extend s1 add ( WITH t as t1: (s1 where t=t1) {ALL BUT t} as v) {t,v}




OPERATOR ts.char (s1 SAME_TYPE_AS  (timeseries)) RETURNS CHARACTER;
BEGIN;
VAR s character init('RELATION {');
VAR coma character init('');
FOR s1 ORDER(ASC t); 
BEGIN;
s := s || coma || '  TUPLE  { t ' ||  t || ' , v ' ||  v || '}';
coma := ',';
END;
END FOR;
s := s ||  '}';
return s;
END;
END OPERATOR;




//------Conjunts--------

//Perinença i inclusió

OPERATOR ts.in( m SAME_TYPE_AS  (timeseries), s1 SAME_TYPE_AS  (timeseries)) RETURNS BOOLEAN;
return (TUPLE from m) IN s1;
END OPERATOR;


OPERATOR ts.in.t( m SAME_TYPE_AS  (timeseries), s1 SAME_TYPE_AS  (timeseries)) RETURNS BOOLEAN;
return (TUPLE from m {t}) IN s1 {t};
END OPERATOR;
 


//inclusio
//inclusio temporal





//Diferència
OPERATOR ts.minus(s1 SAME_TYPE_AS  (timeseries), s2 SAME_TYPE_AS  (timeseries)) RETURNS RELATION SAME_HEADING_AS  (timeseries);
return s1 MINUS s2;
END OPERATOR;

OPERATOR ts.minus.t(s1 SAME_TYPE_AS  (timeseries), s2 SAME_TYPE_AS  (timeseries)) RETURNS RELATION SAME_HEADING_AS  (timeseries);
return s1 MINUS s2 MINUS (s1 JOIN (s1 {t} MINUS s2 {t}));
END OPERATOR;

//Intersecció
OPERATOR ts.intersection(s1 SAME_TYPE_AS  (timeseries), s2 SAME_TYPE_AS  (timeseries)) RETURNS RELATION SAME_HEADING_AS  (timeseries);
return ts.minus(s1, ts.minus(s1,s2));
END OPERATOR;

OPERATOR ts.intersection.t(s1 SAME_TYPE_AS  (timeseries), s2 SAME_TYPE_AS  (timeseries)) RETURNS RELATION SAME_HEADING_AS  (timeseries);
return ts.minus.t(s1, ts.minus.t(s1,s2));
END OPERATOR;

//Diferència simètrica
OPERATOR ts.xor(s1 SAME_TYPE_AS  (timeseries), s2 SAME_TYPE_AS  (timeseries)) RETURNS RELATION SAME_HEADING_AS  (timeseries);
return ts.union(ts.minus(s1, s2), ts.minus(s1, s2));
END OPERATOR;

OPERATOR ts.xor.t(s1 SAME_TYPE_AS  (timeseries), s2 SAME_TYPE_AS  (timeseries)) RETURNS RELATION SAME_HEADING_AS  (timeseries);
return ts.union.t(ts.minus.t(s1, s2), ts.minus.t(s1, s2));
END OPERATOR;




//Producte i junció
OPERATOR ts.product(s1 SAME_TYPE_AS  (timeseries), s2 SAME_TYPE_AS  (timeseries)) RETURNS RELATION SAME_HEADING_AS  (timeseriesdouble);
return (s1 RENAME (t AS t1, v AS v1)) JOIN (s2 RENAME (t AS t2, v AS v2));
END OPERATOR;


OPERATOR ts.join(s1 SAME_TYPE_AS  (timeseries), s2 SAME_TYPE_AS  (timeseries)) RETURNS RELATION SAME_HEADING_AS  (timeseries);
return (s1 RENAME (v AS v1) s2) JOIN (s2 RENAME (v AS v2)) ;
END OPERATOR;




//Computacionals

//map equivalent a: EXTEND s ADD ( <texpr> AS tp, <vexpr> as vp ) {tp,vp} RENAME (tp AS t, vp AS v)

//Per a fer l'execute es necessiten variables globals
VAR ts.map.sp BASE SAME_TYPE_AS ( timeseries) KEY { t };
OPERATOR ts.map(s SAME_TYPE_AS  (timeseries), texpr CHARACTER, vexpr CHARACTER) RETURNS RELATION SAME_HEADING_AS  (timeseries);
BEGIN;
VAR exp character init('');
exp := 'ts.map.sp := extend ' || ts.char(s) || ' ADD ( ' || texpr || ' AS tprima,' || vexpr || ' AS vprima) {tprima,vprima} RENAME (tprima AS t,vprima AS v);';
execute exp;
return ts.map.sp;
END;
END OPERATOR;






//especials per a fer fold 
//com es deu declararar una relacio de tipus RELATION {} i que quadri amb totes?

VAR ts.map.smi BASE RELATION { t RATIONAL, v RATIONAL , ti RATIONAL, vi RATIONAL}  KEY { t } ;

OPERATOR ts.map.mi(s RELATION { t RATIONAL, v RATIONAL, ti RATIONAL, vi RATIONAL }, texpr CHARACTER, vexpr CHARACTER) RETURNS RELATION SAME_HEADING_AS  (timeseries);
BEGIN;
VAR exp character init('');
ts.map.smi := s;
exp := 'ts.map.sp := (extend ts.map.smi  ADD ( ' || texpr || ' AS tprima,' || vexpr || ' AS vprima) {tprima,vprima} RENAME (tprima AS t,vprima AS v) ){t,v};';
execute exp;
return ts.map.sp;
END;
END OPERATOR;



OPERATOR ts.fold(s SAME_TYPE_AS  (timeseries), mi SAME_TYPE_AS  (timeseries), texpr CHARACTER, vexpr CHARACTER ) RETURNS RELATION SAME_HEADING_AS  (timeseries);
BEGIN;
  IF
    ts.isempty(s)
  THEN
    return mi;
  ELSE 
   BEGIN;    
    VAR ma PRIVATE SAME_TYPE_AS ( timeseries) KEY { t };
    VAR m PRIVATE RELATION { t RATIONAL, v RATIONAL , ti RATIONAL, vi RATIONAL}  KEY { t } ;
    ma := ts.min(s);
    s := s MINUS ma;
    m := EXTEND ts.fold(s,mi,texpr,vexpr) ADD (ts.t(ma) as ti, ts.v(ma) as vi);
    return ts.map.mi(m,texpr,vexpr);
   END;
END IF;
END;
END OPERATOR;


OPERATOR ts.mapfold(s SAME_TYPE_AS  (timeseries), si SAME_TYPE_AS  (timeseries), texpr CHARACTER, vexpr CHARACTER ) RETURNS RELATION SAME_HEADING_AS  (timeseries);
return ts.fold(s,si,texpr,vexpr)
END OPERATOR;





//------Seqüències--------


OPERATOR ts.interval(s1 SAME_TYPE_AS  (timeseries), l RATIONAL, h RATIONAL) RETURNS RELATION SAME_HEADING_AS  (timeseries);
return s1 WHERE t>l AND t<=h;
END OPERATOR;

OPERATOR ts.interval.closed(s1 SAME_TYPE_AS  (timeseries), l RATIONAL, h RATIONAL) RETURNS RELATION SAME_HEADING_AS  (timeseries);
return s1 WHERE t>=l AND t<=h;
END OPERATOR;

OPERATOR ts.interval.left(s1 SAME_TYPE_AS  (timeseries), l RATIONAL, h RATIONAL) RETURNS RELATION SAME_HEADING_AS  (timeseries);
return s1 WHERE t>l AND t<=h;
END OPERATOR;


OPERATOR ts.interval.ni(s1 SAME_TYPE_AS  (timeseries), h RATIONAL) RETURNS RELATION SAME_HEADING_AS  (timeseries);
return s1 WHERE t<h;
END OPERATOR;



OPERATOR ts.next( m SAME_TYPE_AS  (timeseries), s1 SAME_TYPE_AS  (timeseries)) RETURNS RELATION SAME_HEADING_AS  (timeseries);
return ts.inf(ts.interval(s1,ts.t(m),1.0/0.0));
END OPERATOR;

OPERATOR ts.prev( m SAME_TYPE_AS  (timeseries), s1 SAME_TYPE_AS  (timeseries)) RETURNS RELATION SAME_HEADING_AS  (timeseries);
return ts.sup(ts.interval.ni(s1,ts.t(m)));
END OPERATOR;








//Temporals



//OPERATOR ts.select.t(s SAME_TYPE_AS  (timeseries), tt RELATION {t RATIONAL}, r OPERATOR ) RETURNS RELATION SAME_HEADING_AS  (timeseries);
//BEGIN:
//VAR si PRIVATE SAME_TYPE_AS ( timeseries) KEY { t };
//sp := RELATION {
//};
//return ts.fold(s, si, texpr CHARACTER, vexpr CHARACTER );
//END;
//END OPERATOR;









//drop
// DROP OPERATOR ts.union(RELATION SAME_HEADING_AS (timeseries),RELATION SAME_HEADING_AS (timeseries));

//DROP VAR timeseries;




//Time Series


//TYPE TIMESERIES POSSREP {T INTEGER, V RATIONAL};
//DROP TYPE TIMESERIES;
//sys.Catalog WHERE Name='sys.Types'
//sys.Types
//sys.Operators



//redistribution FROM TUPLE FROM sys.Version

