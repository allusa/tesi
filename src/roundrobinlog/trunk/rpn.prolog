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



%rrdtool http://oss.oetiker.ch/rrdtool/doc/rrdgraph_rpn.en.html

% Processing the stack directly
o(dup,[V|P],[V,V|P]).
o(pop,[_|P],P).
o(exc,[V1,V2|P],[V2,V1|P]).

o(exc2,[V1,V2,V3|P],[V2,V3,V1|P]).

o(cul,P,[C|P]) :-
	cul(P,C).
o(roda,P,Pr) :-
	roda(P,Pr).



% A,B,C,if -> if A then B else C
o(if,[_,B,1|P],[B|P]).
o(if,[C,_,0|P],[C|P]).

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
	

%---------------------------------------
% operacions sense indefinits
%---------------------------------------

%indefinit 3 operands

o(limit,[i,_,_|P],[i|P]) :- !.
o(limit,[_,i,_|P],[i|P]) :- !.
o(limit,[_,_,i|P],[i|P]) :- !.


% Comparing values

% A,B,C,limit -> A if B =< A =< C
o(limit,[C,B,A|P],[A|P]) :-
	o(le,[A,B],[1]),
	o(le,[C,A],[1]), !.
o(limit,[_,B,A|P],[i|P]) :-
	o(lt,[B,A],[1]), !.
o(limit,[C,_,A|P],[i|P]) :-
	o(lt,[A,C],[1]), !.



%indefinit 2 operands
o(_,[i,_|P],[i|P]) :- !.
o(_,[_,i|P],[i|P]) :- !.


% Boolean operators
% A,B,eq -> A == B
o(eq,[+i,+i|P],[1|P]) :- !.
o(eq,[-i,-i|P],[1|P]) :- !.
o(eq,[+i,_|P],[0|P]) :- !.
o(eq,[_,+i|P],[0|P]) :- !.
o(eq,[-i,_|P],[0|P]) :- !.
o(eq,[_,-i|P],[0|P]) :- !.
o(eq,[+i,_|P],[0|P]) :- !.
o(eq,[B,A|P],[1|P]) :- 
	number(A),
	number(B),
	A =:= B, !. 
o(eq,[B,A|P],[0|P]) :- 
	not( o(eq,[B,A|P],[1|P]) ), !.

% A,B,lt -> A < B
o(lt,[_,+i|P],[0|P])  :- !.
o(lt,[-i,_|P],[0|P])  :- !.
o(lt,[+i,A|P],[1|P])  :-
	o(eq,[+i,A],[0]), !. 
o(lt,[B,-i|P],[1|P])  :-
	o(eq,[B,-i],[0]), !. 
o(lt,[B,A|P],[1|P]) :-
	number(A),
	number(B),
	A < B, !.
o(lt,[B,A|P],[0|P]) :- 
	number(A),
	number(B),
	A >= B, !.

% A,B,gt -> A > B
o(gt,[B,A|P],[0|P]) :-
	o(eq,[B,A],[1]), !.
o(gt,[B,A|P],[0|P]) :-
	o(lt,[B,A],[1]), !.
o(gt,[B,A|P],[1|P]) :-
	o(eq,[B,A],[0]),
	o(lt,[B,A],[0]), !.


% A,B,le -> A =< B
o(le,P,[1|R]) :-
	o(lt,P,[1|R]), !.
o(le,P,[1|R]) :-
	o(eq,P,[1|R]), !.
o(le,P,[0|R]) :-
	o(lt,P,[0|R]),
	o(eq,P,[0|R]), !.
% A,B,ge -> A >= B
o(ge,P,[1|R]) :-
	o(gt,P,[1|R]), !.
o(ge,P,[1|R]) :-
	o(eq,P,[1|R]), !.
o(ge,P,[0|R]) :-
	o(gt,P,[0|R]),
	o(eq,P,[0|R]), !.

% A,B,ne -> A != B
o(ne,P,[0|R]) :-
	o(eq,P,[1|R]), !.	
o(ne,P,[1|R]) :-
	o(eq,P,[0|R]), !.	




% Comparing values
o(min,[B,A|P],[B|P]) :-
	o(lt,[B,A],[0]), !.
o(min,[B,A|P],[A|P]) :-
	o(lt,[B,A],[1]), !.
o(min,[B,A|P],[A|P]) :-
	o(eq,[B,A],[1]), !.

o(max,[B,A|P],[B|P]) :-
	o(gt,[B,A],[0]), !.
o(max,[B,A|P],[A|P]) :-
	o(gt,[B,A],[1]), !.
o(max,[B,A|P],[A|P]) :-
	o(eq,[B,A],[1]), !.


% Arithmetics
o(+,[V1,V2|P],[V|P]) :-
	V is V1+V2.

	





