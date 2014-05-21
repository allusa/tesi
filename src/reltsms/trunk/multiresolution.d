
//multiresolution over TSMS
BEGIN;


OPERATOR mtsms.aaf.maxzohe(
	 s SAME_TYPE_AS  (timeseries), 
	 t0 RATIONAL, 
	 tf RATIONAL)        
	 RETURNS RELATION SAME_HEADING_AS  (timeseries);
  return summarize ts.interval.zohe(s,t0,tf) ADD (max(t) as t, max(v) as v);
END OPERATOR;



//dmap
OPERATOR mtsms.dmap(
	 s SAME_TYPE_AS  (timeseries), 	 
	 delta RATIONAL, 
	 tau RATIONAL,         
	 f CHAR,         
	 k RATIONAL) 
	 RETURNS RELATION SAME_HEADING_AS  (timeseries);
  begin;
    var si private same_type_as ( timeseries) key { t };
    var tmax rational;
    tmax := ts.t(ts.max(s));
    si := ts.generator(tau,tmax+delta,delta)
	    where t > tmax - k*delta and t <= tmax;


    //extend si add ( f(s,t-delta,t) as tvp ) {tvp} ungroup(tvp) //param:
    ts.globalexecute := si;
    ts.globalexecute2 := s;
    var exp char;
    exp := 'ts.globalexecute := extend ts.globalexecute add (' || f || '(ts.globalexecute2,t-' || delta || ',t) as tvp ) {tvp} ungroup(tvp);';
    execute exp;
  
    return ts.globalexecute;
  end;
END OPERATOR;



//multiresolution
OPERATOR mtsms.dmap(
	 s SAME_TYPE_AS  (timeseries), 	 
	 schema SAME_TYPE_AS  (timeseries)) 
	 RETURNS RELATION SAME_HEADING_AS  (timeseries);
  begin;
    var si private same_type_as ( timeseries) key { t };
    
    si := relation {}; 

    //de moment fold = ofold(_,min)
    return ts.fold(schema,si,'','');
  end;
END OPERATOR;


END;
