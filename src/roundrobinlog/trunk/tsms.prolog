
consult('rpn.pl').


% mesura m(t,v1,v2,...)
% mesura(V,T)
m(_,_).
%mesura multivaludada
m(_,[_]).
%temps mesura
t(m(T,_),T).
%valor mesura
v(m(_,V),V).
	

% serie temporal [m0(),m1(),...,mk()]
% conjunt
conj([]).
conj([A|R]) :- 
	not(member(A,R)),
	conj(R).


%operacions conjunt

%pertany -> member predefinit

cardinal([],0).
cardinal([_|R],N) :-
	cardinal(R,Nr),
	N is 1 + Nr. 


diferencia([],_,[]) :- !.
diferencia([X|R],Y,Z) :-
	member(X,Y),
	diferencia(R,Y,Z),!.
diferencia([X|R],Y,[X|Z]) :-
	diferencia(R,Y,Z).


% serie temporal
s([]).
s([A|R]) :- 
	not(pertanyt(A,R)),
	s(R).
    %cal comprovar que tinguin la mateixa dimensio	
	%% mida(A,G),
	%% grau(R,G).

%operacions serie temporal

%grau
grau([],0).
grau([M|_],G) :- length(M,G).

%pertanyença temporal
pertanyt(m(T,_),S) :- member(m(T,_),S).

%mínim
minim([M|[]],M) :- !.
minim([M0|S],M0) :-
	minim(S,M1),
	t(M0,T0),
	t(M1,T1),
	T0 =< T1,!.
minim([_|S],M1) :-
	minim(S,M1).
%màxim
maxim([M|[]],M) :- !.
maxim([M0|S],M0) :-
	maxim(S,M1),
	t(M0,T0),
	t(M1,T1),
	T0 >= T1,!.
maxim([_|S],M1) :-
	maxim(S,M1).

%ínfim	
inf([],m(+i,i)) :- !.
inf(S,M) :- minim(S,M).
%suprem
sup([],m(-i,i)) :- !.
sup(S,M) :- maxim(S,M).


%unio: S1 U S2
%unio(S1,S2,R)
unio(Z,[],Z) :- !.
unio(Y,[X|R],Z) :-
	pertanyt(X,Y),
	unio(Y,R,Z),!.
unio(Y,[X|R],[X|Z]) :-
	unio(Y,R,Z).

%seleccio: S(r,t] 
%interval(S,r,t,R)
interval([],_,_,[]).
%interval(S,-i,+i,S). %excepte S[-i]
interval(S,R,+i,Sr) :-
	%atencio compte quan sup(S) = m(+i,i)
	sup(S,m(T,_)),
	interval(S,R,T,Sr),!.
interval(S,-i,T,Sr) :-
	%atencio compte quan inf(S) = m(-i,i)
	inf(S,M),
	t(M,R),
	interval(S,R-1,T,Sr),!. % R-1 < T(inf(S)) --> T(inf(S)) <= T(m) <= T
interval([M|S],R,T,[M|Sr]) :-
	t(M,Tm),
	R < Tm,
	Tm =< T,
	interval(S,R,T,Sr),!.
interval([_|S],R,T,Sr) :-
	interval(S,R,T,Sr).
intervale(S,-i,T,Sr) :-
	interval(S,-i,T,Si),
	sup(Si,M),
	t(M,T),
	diferencia(Si,[M],Sr),!.
intervale(S,-i,T,Sr) :-
	interval(S,-i,T,Sr).


%seleccio temporal
%selecciot(S,T0,Tf,R)
selecciot(S,T0,Tf,R) :-
	%representació zohe
	interval(S,T0,Tf,Si),
	intervale(S,-i,Tf,Sie),
	diferencia(S,Sie,Sd),
	inf(Sd,m(_,V)),
	unio(Si,[m(Tf,V)],R).

	
%seleccio resolucio
%selecciores(S,T,R)	
selecciores(_,[],[]).
selecciores(S,[T0|T],R) :-
	selecciot(S,T0,T0,St),
	selecciores(S,T,Rr),
	unio(St,Rr,R).

%unió temporal
%uniot(S1,S2,R)
uniot(S1,S2,R) :-
	inf(S1,m(T1,_)),
	sup(S1,m(T2,_)),
	selecciot(S2,T1,T2,S2s),
	diferencia(S2,S2s,S2d),
	unio(S1,S2d,R).


%fusió temporal
%fusiot(S1,S2,R)
temps([],[]). %momentani: per poder treure els temps d'una S
temps([M|S],[Tm|T]) :-
	t(M,Tm),
	temps(S,T).

concatena([],[V|V2],[V|V2]).
concatena([],V,[V]).
concatena([V|V1],V2,[V|R]) :-
	concatena(V1,V2,R).
concatena(V,V2,[V|R]) :-
	concatena([],V2,R).
	

fusio(_,[],[]) :- !.
fusio([M1|C1],[M2|C2],[m(T,V)|C]) :-
	t(M1,T),
	t(M2,T),
	v(M1,V1),
	v(M2,V2),
	concatena(V1,V2,V),
	fusio(C1,C2,C),!.
fusio([M1|C1],[M2|C2],C) :-
	fusio([M2],C1,Cm2),
	fusio([M1|C1],C2,Cm1),
	unio(Cm2,Cm1,C),!.	
fusio(C1,[_|C2],C) :-	
	fusio(C1,C2,C).

fusiot(S1,S2,R) :-
	unio(S1,S2,Su),
	temps(Su,T),
	selecciores(S1,T,S1r),
	selecciores(S2,T,S2r),
	fusio(S1r,S2r,R).
	

%operacions map-fold
%map(S,f(m),R)
map([],_,[]).
map([M|S],F,R) :-
	aplica(M,F,Mf),
	map(S,F,Smap),
	unio([Mf],Smap,R).

%aplica(M,F,Mf)
aplica([C1|C],[F1|F],[M1|Mf]) :-
	rpn(C1,F1,M1),
	aplica(C,F,Mf).



%RPN


	




%Exemples


% s([m(2,1),m(3,2)]).
% pertanyt(m(2,0),[m(2,1),m(3,2)]).
% unio([m(2,1),m(3,2)],[m(2,0),m(1,2)],R).
% interval([m(2,1),m(3,2)],2,3,R).
% selecciot([m(2,1),m(4,2)],1,3,R).
% selecciores([m(1,i),m(2,1),m(4,2)],[0,3,6,7],R).
% uniot([m(2,3),m(4,2),m(6,4)],[m(1,2),m(5,3),m(6,5),m(10,1)],R).
% uniot([m(1,2),m(5,3),m(6,5),m(10,1)],[m(2,3),m(4,2),m(6,4)],R).
% fusiot([m(2,3),m(4,2),m(6,4)],[m(1,2),m(5,3),m(6,5),m(10,1)],R).
