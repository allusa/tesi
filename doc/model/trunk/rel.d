
VAR timeseries BASE RELATION
    { t RATIONAL, v RATIONAL }  KEY { t } ;



OPERATOR ts.t(m SAME_TYPE_AS  (timeseries)) RETURNS RATIONAL;
return t FROM TUPLE FROM m;
END OPERATOR;

OPERATOR ts.v(m SAME_TYPE_AS  (timeseries)) RETURNS RATIONAL;
return v FROM TUPLE FROM m;
END OPERATOR;




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





OPERATOR ts.union(s1 SAME_TYPE_AS  (timeseries), s2 SAME_TYPE_AS  (timeseries)) RETURNS RELATION SAME_HEADING_AS  (timeseries);
return s1 UNION (s2 JOIN (s2 {t} MINUS s1 {t}));
END OPERATOR;

OPERATOR ts.intersect(s1 SAME_TYPE_AS  (timeseries), s2 SAME_TYPE_AS  (timeseries)) RETURNS RELATION SAME_HEADING_AS  (timeseries);
return s1 JOIN (s1 {t} INTERSECT s2 {t});
END OPERATOR;

OPERATOR ts.xunion(s1 SAME_TYPE_AS  (timeseries), s2 SAME_TYPE_AS  (timeseries)) RETURNS RELATION SAME_HEADING_AS  (timeseries);
return ts.union(s1,s2) MINUS ts.intersect(s1,s2) ;
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






//drop
// DROP OPERATOR ts.union(RELATION SAME_HEADING_AS (timeseries),RELATION SAME_HEADING_AS (timeseries));

//DROP VAR timeseries;




//Time Series


//TYPE TIMESERIES POSSREP {T INTEGER, V RATIONAL};
//DROP TYPE TIMESERIES;
//sys.Catalog WHERE Name='sys.Types'
//sys.Types
//sys.Operators

