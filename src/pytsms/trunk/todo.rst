====
ToDo
====

Mesures:

* Haurien de ser més semblants als tuples (o conjunts), tal com les sèries temporals són conjunts


Sèries temporals:

* Cal implementar les formes canòniques, multivaluada i doble i tenir-ho en compte a les operacions. Sobretot cal pensar que passa a les operacions crítiques, com per exemple el join, quan no treballen en la forma canònica.

* Estudiar com afecta la definició de l'operació de pertinença a les altres: unió, add, etc. 

* Estudiar com afecta la definició d'una operació a les altres, per exemple unió a les altres. És a dir, mirar com python implementa els operadors de conjunts si en base a la pertinença, a la unió, etc. i aquesta implementació és coherent amb les necessitats del model SGST. Un cas concret és la relació entre pertinença/igualtat/add: si definim la igualtat entre mesures com eqt() aleshores queda definida la pertinença al conjunt i l'add sense repetits però la igualtat entre sèries temporals no és el que esperaríem que fos amb eqp() entre mesures.


Operacions de seqüència:

* En les implementacions d'interval interval_open(), interval_close(), etc. estaria bé que es poguessin cridar amb None el que ara s'ha de fer amb float("inf"), per exemple  s.interval_open(2,None), tal com ja es pot fer en la implementació amb slices s[2:] i que en la notació SGST és equivalent a s(2,infinit).
