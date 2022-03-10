Programul primeste de la tastatura numele a 
3 fisiere: 
un fisier in care este descris lexerul, un 
fisier cu inputul si un fisier unde trebuie 
sa scrie output-ul.

Pentru transformarea in forma prenex a Regex-ului:
La intalnirea unei paranteze "(", se creeaza 
o noua stiva goala care stocheaza instructiunile.
La intalnirea unei paranteze ")" elementele 
din stiva sunt aduse in forma prenex si 
considerate ca un singur element.
De asemenea, stiva se inchide is "elementul"
este stiva cu un nivel mai jos.
La final, ramane o singura stiva care este
trecuta in forma prenex.
Programul functioneaza atunci cand  expresia 
data este corecta
.

Pentru Transformarea din forma prenex in DFA:
Forma prenex este transformata intr-un NFA 
--- fiecare operatia are functia(STAR,CONCAT,
PLUS,UNION) sa care primeste un numar specific
de operatori si returneaza un NFA echivalent.
NFA-ul este transformat intr-un dfa prin 
intermediul unui algoritm de epsilon closure care 
se foloseste de Depth First Search(DFS) algorithm.
 
Pentru implementarea Lexerului, acesta primeste
un fisier cu specificatia si un fisier cu un 
input (cuvantul) care va fi scanat si returneaza
un fisier care contine un sir de tokens si lexeme
identificate.

Exemplu de functionare:
Fisierul "lexer" contine:
C c;

ABS (ab)+;

BS b*;

Fisierul "input" contine:

abababcb

Comanda excutata este:
runcompletelexer(lexer, input, output) 

Fisierul "output" o sa contina:
ABS ababab
C c

BS b