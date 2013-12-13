


VAR mtsms.buffers BASE RELATION
    {S same_type_as(timeseries), tau RATIONAL, delta RATIONAL, f CHARACTER} KEY { delta, f } ;



VAR mtsms.discs BASE RELATION
    {S same_type_as(timeseries), k RATIONAL, n CHARACTER} KEY { n } ;



OPERATOR mtsms.addB(b SAME_TYPE_AS  (mtsms.buffers),m SAME_TYPE_AS  (timeseries)) RETURNS SAME_TYPE_AS (mtsms.buffers);
   return ts.union(S FROM TUPLE FROM b,m);
END OPERATOR;


OPERATOR mtsms.consolidateB(b SAME_TYPE_AS  (mtsms.buffers)) RETURNS Relation { B SAME_TYPE_AS (mtsms.buffers), m SAME_TYPE_AS (timeseries)};
   return S FROM TUPLE FROM b
END OPERATOR;
