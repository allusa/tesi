


//types or variables

VAR timeseries BASE RELATION
    { t RATIONAL, v RATIONAL }  KEY { t } ;

VAR timeseriesdouble BASE RELATION
    { t1 RATIONAL, v1 RATIONAL, t2 RATIONAL, v2 RATIONAL }  KEY { t1, t2 } ;


//Per a fer l'execute es necessiten variables globals
VAR ts.globalexecute BASE SAME_TYPE_AS ( timeseries) KEY { t };



//operators using Tutorial D:
//multivalued2canonical ->   s group ({all but t} as v)
//canonical2multivalued ->   s ungroup (v)






//measure operators

OPERATOR ts.t(
	 m SAME_TYPE_AS  (timeseries)) 
	 RETURNS RATIONAL;
  return t FROM TUPLE FROM m;
END OPERATOR;

OPERATOR ts.v(
	 m SAME_TYPE_AS  (timeseries)) 
	 RETURNS RATIONAL;
  return v FROM TUPLE FROM m;
END OPERATOR;




//set operators

OPERATOR ts.max(
	 s1 SAME_TYPE_AS  (timeseries))
	 RETURNS RELATION SAME_HEADING_AS  (timeseries);
  return s1 JOIN SUMMARIZE s1 {t} ADD (MAX (t) AS t);
END OPERATOR;

OPERATOR ts.min(
	 s1 SAME_TYPE_AS  (timeseries)) 
	 RETURNS RELATION SAME_HEADING_AS  (timeseries);
  return s1 JOIN SUMMARIZE s1 {t} ADD (MIN (t) AS t);
END OPERATOR;

OPERATOR ts.sup(
	 s1 SAME_TYPE_AS  (timeseries)) 
	 RETURNS RELATION SAME_HEADING_AS  (timeseries);
  return ts.max(ts.union(s1,(RELATION { TUPLE {t -1.0/0.0, v 1.0/0.0} })));
END OPERATOR;

OPERATOR ts.inf(
	 s1 SAME_TYPE_AS  (timeseries)) 
	 RETURNS RELATION SAME_HEADING_AS  (timeseries);
  return ts.min(ts.union(s1,(RELATION { TUPLE {t 1.0/0.0, v 1.0/0.0} })));
END OPERATOR;



OPERATOR ts.union(
	 s1 SAME_TYPE_AS  (timeseries),
	 s2 SAME_TYPE_AS  (timeseries))
	 RETURNS RELATION SAME_HEADING_AS  (timeseries);
  return s1 UNION (s2 JOIN (s2 {t} MINUS s1 {t}));
END OPERATOR;

OPERATOR ts.union.t(
	 s1 SAME_TYPE_AS  (timeseries), 
	 s2 SAME_TYPE_AS  (timeseries)) 
	 RETURNS RELATION SAME_HEADING_AS  (timeseries);
  return (s1 JOIN (s1 {t} MINUS s2 {t})) UNION (s2 JOIN (s2 {t} MINUS s1 {t}));
END OPERATOR;



//set relational operators

//projection 
// s {t}  (not closed on time series)
// s {t,v}
// s {t,v1} (on multivalued time series)

//selection-restriction
// s where t=2.0
// s where v>4.0

//rename
// s rename (t as t1, v as v1)




//seq operators

OPERATOR ts.interval.closed(
	 s1 SAME_TYPE_AS  (timeseries), 
	 l RATIONAL, 
	 h RATIONAL) 
	 RETURNS RELATION SAME_HEADING_AS  (timeseries);
  return s1 WHERE t>=l AND t<=h;
END OPERATOR;

OPERATOR ts.interval.left(
	 s1 SAME_TYPE_AS  (timeseries), 
	 l RATIONAL, 
	 h RATIONAL) 
	 RETURNS RELATION SAME_HEADING_AS  (timeseries);
  return s1 WHERE t>l AND t<=h;
END OPERATOR;





//temporal function operators

OPERATOR ts.interval.zohe(
	 s SAME_TYPE_AS  (timeseries),
	 l RATIONAL, 
	 h RATIONAL ) 
	 RETURNS RELATION SAME_HEADING_AS  (timeseries);
  BEGIN;
    VAR x RATIONAL init(0.0);
    VAR sp PRIVATE SAME_TYPE_AS ( timeseries) KEY { t };
    x := ts.v(ts.inf(ts.interval.closed(s,h,1.0/0.0)));
    sp := RELATION {
      TUPLE {t h, v x}
      };
    return ts.union(ts.interval.left(s,l,h),sp);
  END;
END OPERATOR;



OPERATOR ts.concatenation.t(
	 s1 SAME_TYPE_AS  (timeseries),
	 s2 SAME_TYPE_AS  (timeseries),
 	 repr CHAR)
	 RETURNS RELATION SAME_HEADING_AS  (timeseries);
  BEGIN;
    VAR t1 RATIONAL init(0.0);
    VAR t2 RATIONAL init(0.0);
    VAR exp character init('');

    t1 := ts.t(ts.inf(s1));
    t2 := ts.t(ts.sup(s1));

    //s2p := ts.interval.zohe(s2,t1,t2); //param:   
    ts.globalexecute := s2;
    exp := 'ts.globalexecute := ts.interval.' || repr || '(ts.globalexecute,' || t1 || ',' || t2 || ');';
    execute exp;
  
    return ts.union(s1,s2 minus ts.globalexecute);
  END;
END OPERATOR;



