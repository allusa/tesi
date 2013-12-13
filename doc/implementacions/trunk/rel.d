
VAR timeseries BASE RELATION
    { t RATIONAL, v RATIONAL }  KEY { t } ;



OPERATOR ts.t(m SAME_TYPE_AS  (timeseries)) RETURNS RATIONAL;
return t FROM TUPLE FROM m;
END OPERATOR;

OPERATOR ts.v(m SAME_TYPE_AS  (timeseries)) RETURNS RATIONAL;
return v FROM TUPLE FROM m;
END OPERATOR;





OPERATOR ts.isempty (s1 SAME_TYPE_AS  (timeseries)) RETURNS BOOLEAN;
BEGIN;
  VAR s PRIVATE SAME_TYPE_AS ( timeseries) KEY { t };
  return s = s1;
END;
END OPERATOR;



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

//per fer
//OPERATOR ts.in( m SAME_TYPE_AS  (timeseries), s1 SAME_TYPE_AS  (timeseries)) RETURNS BOOLEAN;
//return ts.inf(ts.interval(s1,ts.t(m),1.0/0.0));
//END OPERATOR;

//OPERATOR ts.in.t( m SAME_TYPE_AS  (timeseries), s1 SAME_TYPE_AS  (timeseries)) RETURNS BOOLEAN;

//inclusio
//inclusio temporal



//Màxim i suprem

OPERATOR ts.max(s1 SAME_TYPE_AS  (timeseries)) RETURNS RELATION SAME_HEADING_AS  (timeseries);
return s1 JOIN ( SUMMARIZE s1 {t} PER (s1 {}) ADD (MAX (t) AS t));
END OPERATOR;

OPERATOR ts.min(s1 SAME_TYPE_AS  (timeseries)) RETURNS RELATION SAME_HEADING_AS  (timeseries);
return s1 JOIN ( SUMMARIZE s1 {t} PER (s1 {}) ADD (MIN (t) AS t));
END OPERATOR;

OPERATOR ts.sup(s1 SAME_TYPE_AS  (timeseries)) RETURNS RELATION SAME_HEADING_AS  (timeseries);
return ts.max(ts.union(s1,(RELATION { TUPLE {t -1.0/0.0, v 1.0/0.0} })));
END OPERATOR;

OPERATOR ts.inf(s1 SAME_TYPE_AS  (timeseries)) RETURNS RELATION SAME_HEADING_AS  (timeseries);
return ts.min(ts.union(s1,(RELATION { TUPLE {t 1.0/0.0, v 1.0/0.0} })));
END OPERATOR;



//Unió
OPERATOR ts.union(s1 SAME_TYPE_AS  (timeseries), s2 SAME_TYPE_AS  (timeseries)) RETURNS RELATION SAME_HEADING_AS  (timeseries);
return s1 UNION (s2 JOIN (s2 {t} MINUS s1 {t}));
END OPERATOR;

OPERATOR ts.union.t(s1 SAME_TYPE_AS  (timeseries), s2 SAME_TYPE_AS  (timeseries)) RETURNS RELATION SAME_HEADING_AS  (timeseries);
return (s1 JOIN (s1 {t} MINUS s2 {t})) UNION (s2 JOIN (s2 {t} MINUS s1 {t}));
END OPERATOR;

//Diferència
OPERATOR ts.minus(s1 SAME_TYPE_AS  (timeseries), s2 SAME_TYPE_AS  (timeseries)) RETURNS RELATION SAME_HEADING_AS  (timeseries);
return s1 MINUS s2;
END OPERATOR;

OPERATOR ts.minus.t(s1 SAME_TYPE_AS  (timeseries), s2 SAME_TYPE_AS  (timeseries)) RETURNS RELATION SAME_HEADING_AS  (timeseries);
return s1 MINUS s2 MINUS (s1 JOIN (s1 {t} MINUS s2 {t}));
END OPERATOR;

//Intersecció
OPERATOR ts.intersection(s1 SAME_TYPE_AS  (timeseries), s2 SAME_TYPE_AS  (timeseries)) RETURNS RELATION SAME_HEADING_AS  (timeseries);
return s1 MINUS (s1 MINUS s2);
END OPERATOR;

OPERATOR ts.intersection.t(s1 SAME_TYPE_AS  (timeseries), s2 SAME_TYPE_AS  (timeseries)) RETURNS RELATION SAME_HEADING_AS  (timeseries);
return s1 MINUS ts.minus.t(s1,s2);
END OPERATOR;

//Diferència simètrica








OPERATOR ts.intersect(s1 SAME_TYPE_AS  (timeseries), s2 SAME_TYPE_AS  (timeseries)) RETURNS RELATION SAME_HEADING_AS  (timeseries);
return s1 JOIN (s1 {t} INTERSECT s2 {t});
END OPERATOR;


OPERATOR ts.xunion(s1 SAME_TYPE_AS  (timeseries), s2 SAME_TYPE_AS  (timeseries)) RETURNS RELATION SAME_HEADING_AS  (timeseries);
return ts.union(s1,s2) MINUS ts.intersect(s1,s2) ;
END OPERATOR;

 




OPERATOR ts.interval(s1 SAME_TYPE_AS  (timeseries), l RATIONAL, h RATIONAL) RETURNS RELATION SAME_HEADING_AS  (timeseries);
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

OPERATOR ts.temporal.in(m SAME_TYPE_AS  (timeseries), s SAME_TYPE_AS  (timeseries)) RETURNS BOOLEAN;
return (TUPLE FROM m {t}) IN (s {t});
END OPERATOR;



OPERATOR ts.temporal.select.zohe(s SAME_TYPE_AS  (timeseries), l RATIONAL, h RATIONAL ) RETURNS RELATION SAME_HEADING_AS  (timeseries);
BEGIN;
VAR x RATIONAL init(0.0);
VAR sp PRIVATE SAME_TYPE_AS ( timeseries) KEY { t };
x := ts.v(ts.inf(s MINUS ts.interval.ni(s,h)));
sp := RELATION {
TUPLE {t h, v x}
};
return ts.union(ts.interval(s,l,h),sp);
END;
END OPERATOR;





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


//Exemples
//WITH RELATION {
//TUPLE { t 2.0, v 3.0 },
//TUPLE { t 4.0, v 2.0 },
//TUPLE { t 6.0, v 4.0 }
// } AS ts1: 
//ts.max(ts1)