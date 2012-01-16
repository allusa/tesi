%RPN

%rpn(expressio,pilainicial,pilaresultant)
rpn([],P,P) :- !.
rpn([O|F],P,R) :-
	o(O,P,Pr),
	rpn(F,Pr,R), !.
	
% pila
pila([]).
empila(O,P,[O|P]).
desempila([_|P],P).
cim([V|_],V).

cul([V],V).
cul([_|P],R) :-
	cul(P,R).
roda([V],[V]).
roda([V1|P],[C,V1|Pr]) :-
	roda(P,[C|Pr]).
	

%operacions
o(V,P,[V|P]) :-
	number(V).


%indefinit
o(_,[i,i|P],[i|P]).
o(_,[i,_|P],[i|P]).
o(_,[_,i|P],[i|P]).


%rrdtool http://oss.oetiker.ch/rrdtool/doc/rrdgraph_rpn.en.html

% Boolean operators
% A,B,lt -> A < B
o(lt,[+i,+i|P],[0|P]) :- !. 
o(lt,[-i,-i|P],[0|P]) :- !. 
o(lt,[+i,_|P],[1|P])  :- !. 
o(lt,[_,+i|P],[0|P])  :- !. 
o(lt,[-i,_|P],[0|P])  :- !. 
o(lt,[_,-i|P],[1|P])  :- !. 
o(lt,[B,A|P],[1|P]) :-
	A < B, !.
o(lt,[B,A|P],[0|P]) :-
	A >= B, !.

o(gt,[B,A|P],[0|P]) :-
	A =:= B, !.
o(gt,P,[1|Pr2]) :-
	o(lt,P,Pr),
	cim(Pr,0),
	desempila(Pr,Pr2), !.
o(gt,P,[0|Pr2]) :-
	o(lt,P,Pr),
	cim(Pr,1),
	desempila(Pr,Pr2), !.


% A,B,C,if -> if A then B else C
o(if,[_,B,1|P],[B|P]).
o(if,[C,_,0|P],[C|P]).
	


% Comparing values
o(min,[V1,V2|P],[V1|P]) :-
	o(lt,[V1,V2|P],Pr),
	cim(Pr,1), !.
o(min,[V1,V2|P],[V2|P]) :-
	o(lt,[V1,V2|P],Pr),
	cim(Pr,0), !.

o(max,[V1,V2|P],[V1|P]) :-
	o(lt,[V1,V2|P],Pr),
	cim(Pr,0), !.
o(max,[V1,V2|P],[V2|P]) :-
	o(lt,[V1,V2|P],Pr),
	cim(Pr,1), !.



% Arithmetics
o(+,[V1,V2|P],[V|P]) :-
	V is V1+V2.

	


% Processing the stack directly
o(dup,[V|P],[V,V|P]).
o(pop,[_|P],P).
o(exc,[V1,V2|P],[V2,V1|P]).

o(exc2,[V1,V2,V3|P],[V2,V3,V1|P]).

o(cul,P,[C|P]) :-
	cul(P,C).
o(roda,P,Pr) :-
	roda(P,Pr).