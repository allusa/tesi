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

cul([V],V).
cul([_|P],R) :-
	cul(P,R).
roda([V],[V]).
roda([V1|P],[C,V1|Pr]) :-
	roda(P,[C|Pr]).
	



%% línia real ampliada
%A=B
equals(+i,+i):- !.
equals(-i,-i):- !.
equals(A,B) :-
	number(A),
	number(B),
	A =:= B.
%A < B
less(-i,B) :- 
	B \== -i, !.
less(A,+i) :- 
	A \== +i, !.
less(A,B)  :-
	number(A),
	number(B),
	A < B.

% C = A+B
suma(+i,-i,i).
suma(-i,+i,i).
suma(+i,B,+i) :- 
	B \== -i.	
suma(-i,B,-i) :- 
	B \== +i.	
suma(A,+i,+i) :- 
	A \== -i.	
suma(A,-i,-i) :- 
	A \== +i.
suma(A,B,C) :-
	number(A),
	number(B),
	C is A+B.	

% C = A-B
resta(+i,+i,i).
resta(-i,-i,i).
resta(+i,B,+i) :-
	B \== +i.	
resta(-i,B,-i) :-
	B \== -i.
resta(A,+i,-i) :-
	A \== +i.	
resta(A,-i,+i) :-
	A \== -i.
resta(A,B,C) :-
	number(A),
	number(B),
	C is A-B.

% C = A*B
multiplica(A,B,C) :-
	number(A),
	number(B),
	C is A*B.

%---------------------------------------
% operacions
%---------------------------------------
%rrdtool http://oss.oetiker.ch/rrdtool/doc/rrdgraph_rpn.en.html

%% operacions sense indefinits

%indefinit 2 operands
o2i([eq,lt,gt,le,ge,ne,min,max,+,-]).
%indefinit 3 operands
o3i([limit]).


%indefinit 2
o(F,[i,_|P],[i|P]) :-
	o2i(L),
	member(F,L), !.
o(F,[_,i|P],[i|P]) :- 
	o2i(L),
	member(F,L), !.

%indefinit 3
o(F,[i,_,_|P],[i|P]) :- 
	o3i(L),
	member(F,L), !.
o(F,[_,i,_|P],[i|P]) :- 
	o3i(L),
	member(F,L), !.
o(F,[_,_,i|P],[i|P]) :- 
	o3i(L),
	member(F,L), !.




%% Value operators
o(V,P,[V|P]) :-
	number(V).
o(+i,P,[+i|P]).
o(-i,P,[-i|P]).
o(i,P,[i|P]).


%% Boolean operators
% A,B,eq -> A == B
o(eq,[B,A|P],[1|P]) :-	
	equals(A,B).
o(eq,[B,A|P],[0|P]) :-	
	not( equals(A,B) ).

% A,B,lt -> A < B
o(lt,[B,A|P],[1|P])  :-
	less(A,B).
o(lt,[B,A|P],[0|P])  :-
	not( less(A,B) ).

% A,B,gt -> A > B
o(gt,[B,A|P],[1|P]) :-
	not( equals(A,B) ),
	not( less(A,B) ).
o(gt,[B,A|P],[0|P]) :-
	equals(A,B).
o(gt,[B,A|P],[0|P]) :-
	less(A,B).

% A,B,le -> A =< B
o(le,[B,A|P],[1|P]) :-
	equals(A,B).
o(le,[B,A|P],[R|P]) :-
	not( equals(A,B) ),
	o(lt,[B,A],[R]).

% A,B,ge -> A >= B
o(ge,[B,A|P],[1|P]) :-
	equals(A,B).
o(ge,[B,A|P],[R|P]) :-
	not( equals(A,B) ),
	o(gt,[B,A],[R]).

% A,B,ne -> A != B
o(ne,P,[0|R]) :-
	o(eq,P,[1|R]).	
o(ne,P,[1|R]) :-
	o(eq,P,[0|R]).	


% unknown
o(un,[i|P],[1|P]) :- !.
o(un,[A|P],[0|P]) :-
	not( o(un,[A|P],[1|P]) ), !.

%infinite
o(isinf,[i|P],[i|P]) :- !.	
o(isinf,[+i|P],[1|P]) :- !.	
o(isinf,[-i|P],[1|P]) :- !.	
o(isinf,[A|P],[0|P]) :-
	not( o(inf,[A|P],[1|P]) ), !.


% A,B,C,if -> if A then B else C
o(if,[_,B,1|P],[B|P]).
o(if,[C,_,0|P],[C|P]).



%% Comparing values
o(min,[B,A|P],[A|P]) :-
	o(le,[B,A],[1]).
o(min,[B,A|P],[B|P]) :-
	o(le,[B,A],[0]).

o(max,[B,A|P],[A|P]) :-
	o(ge,[B,A],[1]).
o(max,[B,A|P],[B|P]) :-
	o(ge,[B,A],[0]).

% A,B,C,limit -> if B =< A =< C then A else unknown
o(limit,[C,B,A|P],[A|P]) :-
	o(le,[A,B],[1]),
	o(le,[C,A],[1]), !.
o(limit,[_,B,A|P],[i|P]) :-
	o(lt,[B,A],[1]), !.
o(limit,[C,_,A|P],[i|P]) :-
	o(lt,[A,C],[1]), !.



%% Arithmetics
o(+,[V1,V2|P],[V|P]) :-
	suma(V1,V2,V).
o(-,[V1,V2|P],[V|P]) :-
	resta(V1,V2,V).
o(*,[V1,V2|P],[V|P]) :-
	multiplica(V1,V2,V).
	

% Processing the stack directly
o(dup,[V|P],[V,V|P]).
o(pop,[_|P],P).
o(exc,[V1,V2|P],[V2,V1|P]).

o(exc2,[V1,V2,V3|P],[V2,V3,V1|P]).

o(<<,P,Pr) :-
	roda(P,Pr).
o(>>,P,Pr) :-
	roda(Pr,P).

o(cul,P,Pr) :-
	o(<<,P,P1),
	o(dup,P1,P2),
	o(>>,P2,Pr).
