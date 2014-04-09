


//tipus o variables

VAR timeseries BASE RELATION
    { t RATIONAL, v RATIONAL }  KEY { t } ;

VAR timeseriesdouble BASE RELATION
    { t1 RATIONAL, v1 RATIONAL, t2 RATIONAL, v2 RATIONAL }  KEY { t1, t2 } ;



//operadors
OPERATOR ts.union(s1 SAME_TYPE_AS  (timeseries), s2 SAME_TYPE_AS  (timeseries)) RETURNS RELATION SAME_HEADING_AS  (timeseries);
return s1 UNION (s2 JOIN (s2 {t} MINUS s1 {t}));
END OPERATOR;
