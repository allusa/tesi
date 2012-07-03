=============================
Defensa Proposta de Tesi 2012
=============================

:author: Aleix Llusà Serra
:date: Juliol 2012
:contact: aleix (a) dipse.upc.edu



Proposta:

:Proposta de Tesi Doctoral: Estudi i modelització dels sistemes de gestió multiresolució de sèries temporals.

:Autor: Aleix Llusà Serra

:Direcció: Teresa Escobet Canal i Sebastià Vila-Marta

:Programa de Doctorat: Automàtica, Robòtica i Visió

:Universitat: Universitat Politècnica de Catalunya

:Data: Juny de 2012




Tribunal:

* Jordi Saludes Closa

* Ramon Pérez Magrané

* Paco del Águila López


Preguntes fetes pels membres del tribunal durant la defensa de la proposta de tesi doctoral el 29 de juny del 2012.

Respostes revisades posteriorment.




Paco del Aguila
---------------

* Com es contempla l'aplicació de diferents interpoladors a les dades?


* Com està pensada la transmissió d'informació en xarxes de sensors de forma distribuïda?





Ramon Pérez
-----------

* Les sèries temporals són equiparables a un senyal?

* Les sèries temporals es troben a quasi tot arreu.

* Hi ha aplicacions de les sèries temporals en altres camps que els citats? Potser fer una classificació de les aplicacions.

* Què es preferiria: crear un model a part del relacional (perquè les
  sèries temporals no es poguessin resoldre amb el model relacional) o
  un model que encaixi amb el relacional i que Date enviï una carta
  acceptant-lo?

   Es prefereix l'encaix. El model relacional té una formalització i
   una potència excel·lents. Els models semblants o pròxims poden
   aprofitar tota aquesta potència i els estudis que s'han fet,
   sobretot pels conceptes laterals dels SGBD: transaccions,
   redundància, seguretat, etc.

   Nosaltres en el disseny del model proposem utilitzar les mateixes
   tècniques que en el model relacional i també les del cas dels
   intervals temporals, amb l'objectiu de ser-hi tant pròxims com
   puguem i sapiguem. 


* En la planificació temporal de la proposta s'ha hagut d'allargar el temps per omplir els dos anys o s'ha hagut d'escurçar-lo per tal d'acomplir-lo?



Jordi Saludes
-------------

* Proposta de Haskell com a llenguatge d'implementació. Python o
  Prolog no són adequats perquè no declaren tipus. Prolog és un
  llenguatge antic i amb poc ús.

   En el nostre cas, només necessitem un llenguatge per a implementar
   els conceptes i provar-los. Per tant, qualsevol llenguatge capaç de
   fer-ho ens és vàlid. La tria d'un de concret la fem per criteris de
   comoditat i tradició: programari lliure, coneixements previs, etc.


* Falta estat de l'art per la multiresolució: algoritmes de pèrdua,
  solucions en altres camps.

   Es pren nota d'estudiar aquest tema. Tenim constància de l'ús de
   multiresolució en el camp dels gràfics informàtics, però no hem
   investigat ja que esperem a iniciar el disseny del model
   multiresolució per mirar fins a quin punt ha de definir propietats
   dels interpoladors o només cal que els sàpiga aplicar i és l'usuari
   qui els ha de definir.
   

* El model de multiresolució presentat a la tesi de màster no és
  bo. Implica pèrdua de la informació al llarg del temps. Potser fer
  que d'un disc la informació salti a un altre en comptes de
  llençar-la. Potser es podrien trobar algoritmes que comprimissin la
  informació més bé.

   Agafant com a referència els algoritmes de compressió, que n'hi ha
   amb pèrdua o sense pèrdua, no n'hi ha cap que sigui ''el millor'':
   tenen avantatges i inconvenients i a cada aplicació es decideix
   quin és millor utilitzar. Els algoritmes amb pèrdua tenen
   l'inconvenient de perdre dades però ho podem mirar com a avantatge
   i dir que és una selecció: és a dir que es decideix quina
   informació és útil i només es conserva aquesta, si bé és cert que
   un cop feta la compressió més endavant no es pot decidir que se'n
   volia una altra.

   Nosaltres plantegem que potser haurem de dissenyar un sistema
   pluginejable. Observant que és l'usuari qui ha de triar quin
   interpolador vol utilitzar, el sistema li oferix la possibilitat de
   definir-se'l i aplicar-lo a les dades.


* Quan hi ha implicat el temps hi ha una tècnica d'implementació anomenada inter.. que podria lligar amb aquesta proposta.

   Es pren nota d'estudiar aquest tema.


* El corrent NoSQL a què crítica: el model relacional? a SQL? a els
  sistemes relacionals?

   En tot cas és el corrent NoSQL que ha d'aclarir les seves posicions. Hi ha
   molta diversitat i no es poden tractar a tots per igual: alguns
   presenten models altres no.


* Article de Codd 1970 ha estat rebutjat.

   El citem en el text per a establir la referència temporal de quan
   es va crear el model relacional. Com a referències bibliogràfiques
   pel model relacional utilitzem les més modernes de Date i Darwen,
   ja que s'han encarregat de divulgar, millorar i assentar els
   conceptes proposats per Codd. Destaquem el Third Manifesto de Date
   i Darwen com a referència del què s'entén per model relacional
   actualment.


* Perquè és interessant estudiar les sèries temporals? Què no poden
  fer els sistemes relacionals per les sèries temporals?

   El model relacional pot modelar les sèries temporals, entenent que
   el model relacional és complet. Ara bé, els sistemes relacionals no
   poden tractar adequadament les sèries temporals: com s'han de fer
   les fusions entre sèries temporals?, el sistemes relacionals per
   resoldre una consulta poden necessitar fer moltes
   fusions. Nosaltres plantegem la multiresolució de les sèries
   temporals: emmagatzemar la informació de forma compacta
   seleccionant-la prèviament: l'usuari decideix uns interpoladors per
   comprimir les dades i una estructura temporal de com les
   emmagatzemarà.


* Què passa amb els intervals temporals i el model relacional? Els
  històrics es poden descriure simplement amb un rang
  temporals. Quines operacions relacionals no es poden aplicar als
  intervals temporals?

   Es convida al públic a seguir el llibre de Date, Darwen i Lorentzos
   (2002) sobre 'temporal data and the relational model'. Una
   explicació profunda dels conceptes d'aquest llibre estaria fora de
   lloc en una defensa, ja que no són propis, i una introducció al
   tema (amb un exemple com s'ha pogut fer) no és suficient per a
   poder-ne observar els detalls.




