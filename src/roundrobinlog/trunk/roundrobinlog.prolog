%% =============
%% RoundRobinlog
%% =============

%% :Author: Aleix Llusà Serra
%% :Contact: aleix@dipse.upc.edu
%% :Version: 0.1a-dev
%% :Date:  2011-10-18
%% :Abstract: Implementació en Prolog d'un SGBD Round Robin (RRD)
%% :Copyright: GPLv3

%% Implementació en Prolog d'un SGBD Round Robin (RRD). És una implementació complementària del model de dades Round Robin descrit al capítol 6 de la tesi de màster.

%% Amb el suport de la Universitat Politècnica de Catalunya (UPC).


% pila
pila(buit).
empila(O,P,empila(O,P)).
desempila(empila(_,P),P).

%conjunt
conj([]).
conj([A|R]) :- 
	not(member(A,R)),
	conj(R).

%operacions conjunt+serie temporal
cardinal([],0).
cardinal([_|R],N) :-
	cardinal(R,Nr),
	N is 1 + Nr. 

unio([],Z,Z).
unio([X|R],Y,Z) :-
	member(X,Y),
	unio(R,Y,Z).
unio([X|R],Y,[X|Z]) :-
	unio(R,Y,Z).

diferencia([],_,[]).
diferencia([X|R],Y,Z) :-
	member(X,Y),
	diferencia(R,Y,Z).
diferencia([X|R],Y,[X|Z]) :-
	diferencia(R,Y,Z).


% mesura(V,T)
mesura(_,_).


% serie temporal
serietemporal([]).
serietemporal(S) :- conj(S).
%% serietemporal([mesura(_,_)|S]) :-
%% 	conj([mesura(_,_)|S]),
%% 	serietemporal(S).

min(serietemporal([mesura(V,T)]),mesura(V,T)).
min(serietemporal([mesura(V,T)|S]), mesura(V,T)) :-
	min(serietemporal(S),mesura(_,Tm)),
	T < Tm.
min(serietemporal([mesura(_,T)|S]), mesura(Vm,Tm)) :-
	min(serietemporal(S),mesura(Vm,Tm)),
	T > Tm.

max(serietemporal([mesura(V,T)]),mesura(V,T)).
max(serietemporal([mesura(V,T)|S]), mesura(V,T)) :-
	max(serietemporal(S),mesura(_,Tm)),
	T > Tm.
max(serietemporal([mesura(_,T)|S]), mesura(Vm,Tm)) :-
	max(serietemporal(S),mesura(Vm,Tm)),
	T < Tm.


interval(serietemporal([]),(_,_),serietemporal([])).	
interval(S,(T0,inf),S2) :-
	max(S,mesura(_,Tmax)),
	interval(S,(T0,Tmax),S2).
interval(serietemporal([mesura(V,T)|S]),(T0,Tf),S3) :-
	T0 < T,
	T < Tf,
	interval(serietemporal(S),(T0,Tf),S2),
	afegeix(mesura(V,T),S2,S3).
interval(serietemporal([mesura(V,T)|S]),(T0,Tf),S3) :-
	T0 < T,
	T = Tf,
	interval(serietemporal(S),(T0,Tf),S2),
	afegeix(mesura(V,T),S2,S3).
interval(serietemporal([mesura(_,_)|S]),(T0,Tf),S2) :-
	interval(serietemporal(S),(T0,Tf),S2).
   
	
	




% buffer(S,TAU,DELTA,F).
buffer(serietemporal(_),_,_,_).

% disc(S,k)
disc(serietemporal(_),_).

% disc round robin
discrr(buffer(_,_,_,_),disc(_,_)).

% base de dades round robin
rrd([]).
rrd([discrr(B,D)|C]):-
	conj([discrr(B,D)|C]),
	rrd(C).




%operacions

%afegeix(M,S,serietemporal([M|S])).
afegeix(M,serietemporal(S),serietemporal(S2)) :- unio([M],S,S2). 
afegeix(M,buffer(S,TAU,DELTA,F),buffer(S2,TAU,DELTA,F)) :- afegeix(M,S,S2).
afegeix(M,disc(serietemporal(S),K),disc(S2,K)) :- 
	cardinal(S,K),
	min(serietemporal(S),Mmin),
	diferencia(S,[Mmin],Sk),
	afegeix(M,serietemporal(Sk),S2).
afegeix(M,disc(S,K),disc(S2,K)) :- 
	afegeix(M,S,S2).
afegeix(M,discrr(B,D),discrr(B2,D)) :-
	afegeix(M,B,B2).
	
	

%interpoladors zohe
sumav([],0).
sumav([mesura(V,_)|S],R) :-
	sumav(S,Rs),
	R is V + Rs.
	
mitjana(S,(T0,Tf),mesura(V,Tf)) :-
	interval(S,(T0,Tf),serietemporal(S2)),
	sumav(S2,Sv),
	cardinal(S2,N),
	V is Sv/N.
	


	
% consolida
consolidable( buffer(S,Tau,Delta,_) ) :-
	max(S,mesura(_,Tmax)),
	Tmax > Tau + Delta.
consolidable( buffer(S,Tau,Delta,_) ) :-
	max(S,mesura(_,Tmax)),
	Tmax is Tau + Delta.
consolidable(discrr(B,_)) :-
	consolidable(B).


consolida( buffer(S,Tau,Delta,F),buffer(S2,Tau2,Delta,F),M) :-
	consolidable( buffer(S,Tau,Delta,F) ),
	Tau2 is Tau+Delta,
	interval(S,(Tau2,inf),S2),
	Function=..[F,S,(Tau,Tau2),M],
	call(Function).
consolida( discrr(B,D),discrr(B2,D2) ) :-
	consolida(B,B2,M),
	afegeix(M,D,D2).


neg(A,B):-B is -A.




% jocs de proves
% reconsult('roundrobinlog.prolog').
% min(serietemporal([mesura(1,3),mesura(1,2)]),M).
% interval(serietemporal([mesura(0,2),mesura(0,3)]),(0,3),S).
% afegeix(2,serietemporal([]),S1), afegeix(3,S1,S2).
% afegeix(2,buffer(serietemporal([]),2,3,4),B1),afegeix(3,B1,B2).
% afegeix(mesura(0,2),disc(serietemporal([]),2),D1),afegeix(mesura(0,3),D1,D2), afegeix(mesura(0,4),D2,D3).
% consolidable(buffer(serietemporal([mesura(0,2),mesura(0,3),mesura(0,5)]),0,5,2)).
% consolida(buffer(serietemporal([mesura(1,2),mesura(2,3),mesura(0,6)]),0,5,mitjana),B,M).
% rrd([discrr(buffer(serietemporal([]),2,3,4),disc(serietemporal([]),2))]).
% rrd([discrr(buffer(serietemporal([]),2,3,4),disc(serietemporal([]),2)),discrr(buffer(serietemporal([]),2,3,5),disc(serietemporal([]),2))]).