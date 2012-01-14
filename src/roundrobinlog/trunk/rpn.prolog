%RPN

%rpn(expressio,pilainicial,pilaresultant)
rpn([],P,P).
rpn([O|F],P,R) :-
	o(O,P,Pr),
	rpn(F,Pr,R).
	
% pila
pila(buit).
empila(O,P,empila(O,P)).
desempila(empila(_,P),P).
cim(empila(V,_),V).


%operands
op1(P,Pr,V1) :-
	cim(P,V1),
	desempila(P,Pr).	

op2(P,Pr,V1,V2) :- 
	op1(P,P1,V1),
	op1(P1,Pr,V2).

%operacions
o(V,P,R) :-
	number(V),
	empila(V,P,R).

o(+,P,R) :-
	op2(P,Pr,V1,V2),
	V is V1+V2,
	empila(V,Pr,R).

	