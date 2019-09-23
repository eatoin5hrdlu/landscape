% Intelligent Design has no future

:- set_prolog_flag(double_quotes, codes).


					    
aa = [    'Ala',    'Arg',    'Asn',    'Asp',    'Asx',    'Cys',    'Glu',
          'Gln',    'Glx',    'Gly',    'His',    'Ile',    'Leu',    'Lys',
          'Met',    'Phe',    'Pro',    'Ser',    'Pro',    'Thr',    'Trp',
          'Tyr',    'Val' ]
a(1).
ac(5).
at(3).
ag(9).

c(4).
ca(5).
cg(12).
ct(6).

t(2).
ta(9).
tc(6).
tg(10).

g(8).
ga(9).
gc(12).
gt(10).


% Alignment to HMM Profile

seq(1, [m,a,g,g,e,f,l,r,s,r,a]).
seq(2, [m,a,g,g,e,f,l,r,s,r,a]).
seq(3, [m,a,g,g,e,f,l,r,s,r,a]).
seq(4, [m,a,g,g,e,c,l,r,s,r,a]).
seq(5, [m,a,g,g,e,f,l,r,s,r,-,a]).
seq(6, [m,a,c,g,e,f,l,r,s,r,-,a]).
seq(7, [m,a,g,g,e,f,l,r,s,r,-,a]).
seq(8, [m,a,g,g,-,e,f,l,r,s,r,a]).
seq(9, [m,a,g,g,d,e,f,l,r,s,r,a]).
seq(10,[m,c,g,g,e,f,l,r,s,r,a,a]).

exrows([ [m,a,g,g,e,f,l,r,s,r,a],
	 [m,a,g,g,e,f,l,r,s,r,a],
	 [m,a,g,g,e,f,l,r,s,r,a],
	 [m,a,g,g,e,c,l,r,s,r,a],
	 [m,a,g,g,e,f,l,r,s,r,-,a],
	 [m,a,c,g,e,f,l,r,s,r,-,a],
	 [m,a,g,g,e,f,l,r,s,r,-,a],
	 [m,a,g,g,-,e,f,l,r,s,r,a],
	 [m,a,g,g,d,e,f,l,r,s,r,a],
	 [m,c,g,g,e,f,l,r,s,r,a,a] ]).

e2([ [m,a,g],
     [m,a,r] ]).

test :-
%    exrows(M),
    e2(M),
    rows2cols(M,NM),
    write(matrix(NM)).
    
rows2cols([],[]).
rows2cols([R|Rows], [Col|Cs]) :-
    column(Rows, R, Col, Next),
    rows2cols(Next, Cs).

column(       [], [CH|R0],       R0,     [CH]).
column([R1|Rest], [CH|R0],  [R0|New], [CH|CT]) :-
    column(Rest, R1, New, CT).

%column(             [],      [],             []) :- !.
%column([[CH|Row]|Rows], [CH|CT], [Row|RestRows]) :- !, column(Rows, CT, RestRows).
%column(      [[]|Rows],      [],           Rows).



portray(matrix(M)) :-
    portray_matrix(M).

portray_matrix([R|Rs]) :-
    print(R),
    portray(matrix(Rs)).
portray_matrix([]).

spaces([]).
spaces([-|T]) :- spaces(T).

pad([],Len,Tail) :-
    length(Tail,Len),
    spaces(Tail).
pad([H|L1],Len,[H|L2]) :-
    NewLen is Len-1,
    pad(L1,NewLen,L2).

all_same_length(Lists,NewLists) :-
    findall(N,(member(L,Lists), length(L,N)), Sizes),
    max_list(Sizes,Max),
    same_length(Lists,Max,NewLists).

same_length([],_,[]).
same_length([H|T],Max,[NH|NT]) :-
    pad(H,Max,NH),
    same_length(T,Max,NT).

align2HMM(Sequences, HMM) :-
    length(Sequences, Ns),
    Sequences = [First|_Rest],
    length(First, Nl),
    align2HMM(Ns, Nl, Sequences, HMM).


align2HMM(_Ns, _Nl, Sequences, Sequences). % NYI


main :-
    findall(S,seq(_N,S), Ss),
    all_same_length(Ss,Padded),
    align2HMM(Padded,HMM),
    findall(L,(member(L,HMM),writeln(L)),_).

aa('Alanine','A',a,1,).
aa('Arginine','R',r,2).
aa('Asparagine','N',n,3).
aa('Aspartic acid (Aspartate)','D',d,4).
aa('Cysteine','C',c,5).
aa('Glutamine','Q',q,6).
aa('Glutamic acid (Glutamate)','E',e,7).
aa('Glycine','G',g,8).
aa('Histidine','H',h,9).
aa('Isoleucine','I',i,10).

aa('Leucine','L',l,11).
aa('Lysine','K',k,12).
aa('Methionine','M',m,13).
aa('Phenylalanine','F',f,14).
aa('Proline','P',p,15).
aa('Serine','S',s,16).
aa('Threonine','T',t,17).
aa('Tryptophan','W',w,18).
aa('Tyrosine','Y',y,19).
aa('Valine','V',v,20).
aa('Asparagine or Aspartic acid (Aspartate)','B',b,21).
aa('Glutamine or Glutamic acid (Glutamate)','Z',z,22).
aa('Unknown amino acid (any amino acid)','X',x,23).
aa('Translation stop','*','.',24).
aa('Gap of indeterminate length','-','_',25).

a(1). t(2). c(4). g(8).
h(7).
r(9).
y(6).
n(15).

codon(1) --> [1,4,15].
codon(2) --> [8,4,15].
codon(2) --> [1,8,9].
codon(3) --> [1,1,6].
codon(4) --> [8,1,6].
codon(5) --> [2,8,6].
codon(6) --> [4,1,9].
codon(7) --> [8,1,9].
codon(8) --> [8,8,15].
codon(9) --> [4,1,6].
codon(10)--> [1,2,7].
codon(11)--> [6,2,9].
codon(11)--> [4,2,15].
codon(12)--> [1,1,9].
codon(13)--> [1,2,8]. % Start Met
codon(14)--> [2,2,6].
codon(15)--> [4,4,15].
codon(16)--> [2,4,15].
codon(16)--> [1,8,6]. % Serine
codon(17)--> [1,4,15].%Thr
codon(18)--> [2,8,8]. %Tryptophan W
codon(19)--> [2,1,6]. %Tyr  Y
codon(20)--> [8,2,15].%Val  V
codon(21)--> [2,9,1]. % Stop
codon(21)--> [2,1,8]. % Stop

rcodon(1) --> [15,4,1].
rcodon(2) --> [15,4,8].
rcodon(2) --> [9,8,1].
rcodon(3) --> [6,1,1].
rcodon(4) --> [6,1,8].
rcodon(5) --> [6,8,2].
rcodon(6) --> [9,1,4].
rcodon(7) --> [9,1,8].
rcodon(8) --> [15,8,8].
rcodon(9) --> [6,1,4].
rcodon(10)--> [7,2,1].
rcodon(11)--> [9,2,6].
rcodon(11)--> [15,2,4].
rcodon(12)--> [9,1,1].
rcodon(13)--> [8,2,1]. % Start Met
rcodon(14)--> [6,2,2].
rcodon(15)--> [15,4,4].
rcodon(16)--> [15,4,2].
rcodon(16)--> [6,8,1]. % Serine
rcodon(17)--> [15,4,1].%Thr
rcodon(18)--> [8,8,2]. %Tryptophan W
rcodon(19)--> [6,1,2]. %Tyr  Y
rcodon(20)--> [15,2,8].%Val  V
rcodon(21)--> [1,9,2]. % Stop
rcodon(21)--> [8,1,2]. % Stop

%dualcodon(F,R) --> [N,N,N].

dualcodon(1,1) --> [1,4,1].  % aa(1) in either direction
dualcodon(2,2) --> [8,4,8].  % aa(2) in either direction
dualcodon(2,2) --> [1,8,1].  % aa(2) in either direction
dualcodon(3,6) --> [1,1,2].
dualcodon(3,21)--> [1,1,2].


a(1).
ac(5).
at(3).
ag(9).

c(4).
t(2).
g(8).
ca(5).
cg(12).
ct(6).

t(2).
g(8).
ta(9).
tc(6).
tg(10).

g(8).
ga(9).
gc(12).
gt(10).


trans([P1|P1s],[P2|P2s]) --> codon(P1)
