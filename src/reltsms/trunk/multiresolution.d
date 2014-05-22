
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
OPERATOR mtsms.multiresolution(
	 s SAME_TYPE_AS  (timeseries), 	 
	 schema relation {delta rational, tau rational, f char, k rational}) 
	 RETURNS RELATION SAME_HEADING_AS  (timeseries);
  begin;
    var si private same_type_as ( timeseries) key { t };
    
    si := relation {t rational, v rational} {}; 


    //de moment fold = ofold(_,min)return ts.fold(schema,si,'','');

    IF
      IS_EMPTY(schema)
    THEN
      return si;
    ELSE 
      BEGIN;    
        VAR scho PRIVATE SAME_TYPE_AS (schema) KEY { delta };
        VAR schemap PRIVATE SAME_TYPE_AS ( schema) KEY { delta };

      	scho := summarize schema add (min(delta) as delta) join schema;
      	schemap := schema minus scho;

	VAR delta init(delta from tuple from scho);
	VAR tau init(tau from tuple from scho);
	VAR f init(f from tuple from scho);
	VAR k init(k from tuple from scho);

	si :=  mtsms.multiresolution(s,schemap);
      	return ts.concatenation(
	                    mtsms.dmap(s,delta,tau,f,k),
		            si
	        	  );


      	return ts.concatenation(
	                    mtsms.dmap(s,delta,tau,f,k),
		            si
	        	  );
      END;
    END IF;

  end;
END OPERATOR;




END;
