from locale import atoi
from typing import Dict, List


Conf = (int, str)

class DFA:
    def __init__(self, alphabet, initialState, delta, finalStates, nume):
        self.alphabet: List[str] = alphabet
        self.initialState: int = initialState
        self.delta: Dict[int, Dict[str, int]] = delta
        self.finalStates: List[int] = finalStates
        self.nume: str = nume

    def step(self, conf: Conf) -> Conf:
        init = conf[1][0]
        if conf[0] in self.delta:

            for elem in self.delta[conf[0]]:
                if init in elem:

                    t = list(elem.values())
                    return t[0], conf[1][1:]

        return conf[0], conf[1][1:]

    def accept(self, word: str) -> bool:

        conf = (self.initialState, word)
        while conf[1]:
            if conf[1][0] in self.alphabet:
                conf = self.step(conf)
            else:
                return False
        return conf[0] in self.finalStates


def tolist(cuvant) -> List[str]:
    list = []
    isNewLine = 0
    cuvant_iter = iter(cuvant)
    for litera in cuvant_iter:
        if litera == '\\':
            isNewLine = 1

        if isNewLine == 0:
            list.append(litera)
        else:
            list.append("\n")
            isNewLine = 0
            next(cuvant_iter)

    return list

#handles reading and arranging the input into a usable form

def citire(input) -> DFA:
    delta = {}
    nume = input[1]
    alphabet = tolist(input[0])
    input = input[2:]
    init_state = atoi(input[0])

    for i in range(1, len(input) - 1):
        elem = input[i].split(",")
        elem[1] = elem[1][1:-1]
        if(elem[1]) == "\\n":
            elem[1] = "\n"

        d = {elem[1]: atoi(elem[2])}
        if atoi(elem[0]) in delta:
            delta[atoi(elem[0])].append(d)
        else:
            delta[atoi(elem[0])] = [d]

    states = input[len(input) - 1].split()
    final_states = []
    for elem in states:
        elem = atoi(elem)
        final_states.append(elem)

    dfa = DFA(alphabet, init_state, delta, final_states, nume)
    return dfa


def IsInGrammer(word, dfas, out) -> bool:
    for dfa in dfas:
        if (dfa.accept(word)):
            if word == "\n":
                word = "\\n"
            print (dfa.nume + " " + word, file=out)
            return True
    return False


def consumeLetter(word, dfa, foutput):
    with open(foutput, "w") as out:
        copie = word
        cuv2 = ""
        wordSize = len(word)
        ok = 2
        currentLocation = 0
        while copie:

            if (IsInGrammer(copie, dfa, out)):
                currentLocation = wordSize
                copie = word[wordSize:]
                wordSize = len(word)
                ok = 1
            else:
                wordSize = wordSize - 1
                copie = copie[:-1]
                ok = 0

    if ok == 0:
        with open(foutput, "w") as out:
            print ("No viable alternative at character ", file=out, end='')
            print(currentLocation, file=out, end='')
            print (", line 0", file=out, end='')


def runlexer(lexer, finput, foutput):

    dfa = []
    with open(lexer, "r") as input:
        dectit = input.read()
        partitionat = dectit.split("\n\n")
        for elem in partitionat:
            ceva = elem.split("\n")
            dfa.append(citire(ceva))

    with open(finput, "r") as input:
        cuvantul = input.read()
        consumeLetter(cuvantul, dfa, foutput)


#if __name__ == '__main__':
