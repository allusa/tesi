





//DEFINIR TIMESERIES COM A TIPUS


TYPE ts POSSREP {ts relation {t rational, v rational}};



TYPE ts2 IS { ts POSSREP { ts2 relation {t rational, v rational} }};


type provats2 
	POSSREP ts {ts relation {t rational, v relation {v1 rational,v2 rational }}}
	POSSREP multivalued2 {multivalued2 relation {t rational ,v1 rational, v2 rational}} 
	INIT ts (multivalued2:= ts ungroup (v))
	      multivalued2 (ts:= multivalued2 group ({all but t} as v));

//Ex
//with multivalued2(relation{ tuple{ t 1.0, v1 2.0, v2 3.0} }) as r:
//THE_multivalued2(r)

//with multivalued2(relation{ tuple{ t 1.0, v1 2.0, v2 3.0} }) as r:
//THE_ts(r)

//with ts(relation{ tuple{ t 1.0, v relation { tuple {v1 2.0, v2 3.0}} }}) as r:
//THE_multivalued2(r)




//Operador redefinit segons el tipus timeseries

OPERATOR tstype.union(
      s1 timeseries, 
      s2 timeseries) 
      RETURNS timeseries;
  return timeseries(ts.union(THE_ts(s1),THE_ts(s2)));
END OPERATOR;