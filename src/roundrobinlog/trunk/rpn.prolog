%RPN

%rpn(expressio,pilainicial,pilaresultant)
rpn([],P,P).
rpn([O|F],P,R) :-
	o(O,P,Pr),
	rpn(F,Pr,R).
	
% pila
pila([]).
empila(O,P,[O|P]).
desempila([_|P],P).
cim([V|_],V).


%operands
op1(P,Pr,V1) :-
	cim(P,V1),
	desempila(P,Pr).	

op2(P,Pr,V1,V2) :- 
	op1(P,P1,V1),
	op1(P1,Pr,V2).

%operacions
o(V,P,[V|P]) :-
	number(V).

o(+,[V1,V2|P],[V|P]) :-
	V is V1+V2.

	



