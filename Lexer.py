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
    out = []
    ok = 1
    cuvant_iter = iter(cuvant)
    for litera in cuvant_iter:
        if litera == '\\':
            ok = 0

        if ok == 1:
            out.append(litera)
        else:
            out.append("\n")
            ok = 1
            next(cuvant_iter)

    return out


def citire(lines, output) -> DFA:
    delta = {}

    nume = lines[1]

    alp = tolist(lines[0])
    lines = lines[2:]

    init_state = atoi(lines[0])

    for i in range(1, len(lines) - 1):
        elem = lines[i].split(",")

        elem[1] = elem[1][1:-1]
        if(elem[1]) == "\\n":
            elem[1] = "\n"
        d = {elem[1]: atoi(elem[2])}

        if atoi(elem[0]) in delta:
            delta[atoi(elem[0])].append(d)
        else:
            delta[atoi(elem[0])] = [d]
    states = lines[len(lines) - 1].split()
    final_states = []
    for elem in states:
        elem = atoi(elem)
        final_states.append(elem)

    dfa = DFA(alp, init_state, delta, final_states, nume)

    return dfa


def verificare(cuv2, dfa, out) -> bool:
    a = {cuv2: cuv2}

    for ccc in a:
        cuv2 = ccc

    for dfa1 in dfa:
        if (dfa1.accept(cuv2)):
            if cuv2 == "\n":
                cuv2 = "\\n"
            print (dfa1.nume + " " + cuv2, file=out)
            return True

    return False


def mananca(cuvant, dfa, foutput):
    with open(foutput, "w") as out:
        copie = cuvant
        cuv2 = ""
        i = len(cuvant)
        ok = 2
        c = 0
        while copie:

            if (verificare(copie, dfa, out)):
                c = i
                copie = cuvant[i:]
                i = len(cuvant)
                ok = 1

            else:
                i = i - 1

                copie = copie[:-1]
                ok = 0

    if ok == 0:
        with open(foutput, "w") as out:
            print ("No viable alternative at character ", file=out, end='')
            print(c, file=out, end='')
            print (", line 0", file=out, end='')


def runlexer(lexer, finput, foutput):

    dfa = []

    with open(lexer, "r") as input:

        dectit = input.read()
        partitionat = dectit.split("\n\n")
        for elem in partitionat:
            ceva = elem.split("\n")
            dfa.append(citire(ceva, foutput))

    with open(finput, "r") as input:
        cuvantul = input.read()

        mananca(cuvantul, dfa, foutput)


if __name__ == '__main__':

    print(dfa.accept("ab"))
