from Lexer import runlexer
import sys

# part 1: Prenex Regex to Dfa


class NFA:
    def __init__(self, initialState, delta, finalState, nrstari, alph):
        self.initialState: int = initialState
        self.delta: Dict[int, Dict[str, int]] = delta
        self.finalState: int = finalState
        self.alph: [str] = alph
        self.nrstari: int = nrstari


def var(litera) -> NFA:
    init_state = 0
    finalState = 1
    tranzitie = [litera, finalState]
    delta = [init_state, tranzitie]
    nfa = NFA(init_state, delta, finalState, finalState, [])
    return nfa


def plusul(op) -> NFA:
    init_state = op.finalState + 1
    finalState = op.finalState + 2
    epTranzF = ["", op.initialState]
    epTranzDF = ["", finalState]
    delta = op.delta + [init_state, epTranzF] + \
        [op.finalState, epTranzF] + [op.finalState, epTranzDF]
    nfa = NFA(init_state, delta, finalState, finalState, [])
    return nfa


def starr(op) -> NFA:
    init_state = op.finalState + 1
    finalState = op.finalState + 2
    epTranzF = ["", op.initialState]
    epTranzDF = ["", finalState]
    delta = op.delta + [init_state,
                        epTranzF] + [init_state,
                                     epTranzDF] + [op.finalState,
                                                   epTranzF] + [op.finalState,
                                                                epTranzDF]
    nfa = NFA(init_state, delta, finalState, finalState, [])
    return nfa


def union(opUnu, opDoi) -> NFA:
    state = 0
    delta = []
    for tranz in opDoi.delta:
        if isinstance(tranz, int):
            state = tranz + opUnu.finalState + 1
            pass
        else:
            tranz[1] = tranz[1] + opUnu.finalState + 1
            delta = delta + [state, tranz]
    epstranzU = ["", opUnu.initialState]
    epstranzD = ["", opDoi.initialState + opUnu.finalState + 1]
    epsilon = [opDoi.finalState + opUnu.finalState + 2, epstranzU] + \
        [opDoi.finalState + opUnu.finalState + 2, epstranzD]
    tranzitiePart = opUnu.delta + delta + epsilon
    transfinalaD = opUnu.finalState + opDoi.finalState + 1
    epTransFinal = ["", opDoi.finalState + opUnu.finalState + 3]
    epFinal = [transfinalaD, epTransFinal] + [opUnu.finalState, epTransFinal]
    TranzitiiFinale = tranzitiePart + epFinal
    stareFinala = opDoi.finalState + opUnu.finalState + 3
    stareInitiala = opDoi.finalState + opUnu.finalState + 2
    nfa = NFA(stareInitiala, TranzitiiFinale, stareFinala, stareFinala, [])
    return nfa


def concat(opUnu, opDoi) -> NFA:
    init_state = opUnu.initialState
    initdoi = opDoi.initialState
    state = 0
    delta = []
    for tranz in opDoi.delta:
        if isinstance(tranz, int):
            state = tranz + opUnu.finalState + 1
            pass
        else:
            nr = tranz[1] + opUnu.finalState + 1
            tranzfinla = [tranz[0], nr]
            delta = delta + [state, tranzfinla]
    epstranz = ["", initdoi + opUnu.finalState + 1]
    epsilon = [opUnu.finalState, epstranz]
    tranzitiePart = opUnu.delta + delta + epsilon
    finalState = opDoi.finalState + opUnu.finalState + 1
    nfa = NFA(init_state, tranzitiePart, finalState, finalState, [])
    return nfa


def nrOp(expr) -> int:
    if expr == 'STAR':
        return 1
    if expr == 'PLUS':
        return 2

    if expr == 'CONCAT':
        return 3
    if expr == 'UNION':
        return 4
    if len(expr) == 1:
        return 0
    return 60


def splituire(stringu):
    a = stringu.split(" ")
    b = []
    ok = 1
    for elem in a:
        if (elem == "'") & (len(elem) == 1):
            if(ok == 1):
                elem = "' '"
                ok = 0
            else:
                ok = 1
                continue
        b.append(elem)
    return b


def toafn(input) -> NFA:
    with open(input, "r") as input:
        line = input.readlines()
        elemente = splituire(line[0])
        stivaExp = []
        stivaOperanzi = []
        alph = []
        for cuvant in elemente:
            stivaExp.append(cuvant)
            if len(cuvant) == 1:
                if cuvant not in alph:
                    alph.append(cuvant)
            if cuvant[0] == "'":
                alph.append(cuvant[1:-1])
                stivaExp.pop()
                stivaExp.append(cuvant[1:-1])
        while stivaExp:
            a = stivaExp.pop()
            if nrOp(a) == 1:
                op = stivaOperanzi.pop()
                Stea = starr(op)
                stivaOperanzi.append(Stea)
            if nrOp(a) == 2:
                op = stivaOperanzi.pop()
                Stea = plusul(op)
                stivaOperanzi.append(Stea)
            if nrOp(a) == 3:
                ounu = stivaOperanzi.pop()
                odoi = stivaOperanzi.pop()
                conc = concat(ounu, odoi)
                stivaOperanzi.append(conc)
            if nrOp(a) == 4:
                ounu = stivaOperanzi.pop()
                odoi = stivaOperanzi.pop()
                Union = union(ounu, odoi)
                stivaOperanzi.append(Union)
            if nrOp(a) == 0:
                stivaOperanzi.append(var(a))
            if nrOp(a) == 60:
                stivaOperanzi.append(var(a))
    deRet = stivaOperanzi.pop()
    deRet.alph = alph
    return deRet


# Using a Python dictionary to act as an adjacency list


def dfs(visited, graph, node):
    if node not in visited:
        visited.add(node)
        if node in graph.delta:
            for neighbour in graph.delta[node]:
                if (neighbour[0] == ""):
                    dfs(visited, graph, neighbour[1])


def step(lista, carac, nfa, trans):
    ult = []
    for elem in lista:
        if(elem in nfa.delta):
            for tranz in nfa.delta[elem]:
                if carac in tranz:
                    var = tranz[1]
                    ult = list(trans[var])
                    if ult == []:
                        return [var]
    return ult


def recurs(nfa, stare_actuala, trans, newDelta):
    if stare_actuala == []:
        return newDelta
    for carac in nfa.alph:
        stare_urm = step(stare_actuala, carac, nfa, trans)
        if stare_urm == []:
            # handles synca states:
            tranzitie = [carac, [99]]
            d = [stare_actuala, tranzitie]
            newDelta = newDelta + d
        else:
            if True:
                okayyyy = 1
                for i in range(len(newDelta)):
                    if newDelta[i] == stare_actuala:
                        if (carac in newDelta[i + 1]):
                            if newDelta[i + 1][1] == stare_urm:
                                tranzitie = [carac, stare_urm]
                                d = [stare_actuala, tranzitie]
                                newDelta = newDelta + d
                                okayyyy = 0
                if okayyyy == 1:
                    tranzitie = [carac, stare_urm]
                    d = [stare_actuala, tranzitie]
                    newDelta = newDelta + d
                    newDelta = recurs(nfa, stare_urm, trans, newDelta)
    return(newDelta)


def closure(nfa, closers, states):
    newDelta = []
    newDelta = recurs(nfa, list(closers[nfa.initialState]), closers, newDelta)
    for x in nfa.alph:
        tranzitie = [x, [99]]
        d = [[99], tranzitie]
        newDelta = newDelta + d
    deltaAproapeFinal = []
    for state in newDelta:
        ok = 1
        for x in nfa.alph:
            if x in state:
                tranzitie = state
                nrCrt = 0
                for element in tranzitie[1]:
                    nrCrt = nrCrt * 100 + element
                ok = 0
                tranzapp = [tranzitie[0], nrCrt]
                d = [retinut, tranzapp]
                deltaAproapeFinal = deltaAproapeFinal + d

        if ok == 1:
            retinut = 0
            for element in state:
                retinut = retinut * 100 + element
    return(deltaAproapeFinal)


def findIN(lista, uint):
    for x in range(len(lista)):
        if lista[x] == uint:
            return x
            pass
    return -1


def verificare(intunu, intdoi):
    intunu = intunu * (-1)
    if intunu == 0:
        if intdoi == 0:
            return 1
        return 0
    while intunu > 0:
        if intunu == intdoi:
            return 1
        if intunu % 100 == intdoi:
            return 1
        else:
            intunu = intunu // 100
        pass
    return 0


def toDFN(nfa) -> NFA:
    delta = {}
    ok = 0
    for tranz in nfa.delta:
        if isinstance(tranz, int):
            state = tranz
            pass
        else:
            if state in delta:
                delta[state].append(tranz)
            else:
                delta[state] = [tranz]
                ok = ok + 1
    nfa.delta = delta
    vect = []
    for x in range(100):
        vect.append([])

    for st in nfa.delta:
        visited = set()
        dfs(visited, nfa, st)
        vect[st] = visited
    listaS = [nfa.initialState]
    newDelta = closure(nfa, vect, listaS)
    delta = {}
    Stari = []
    nr = 0
    stare_initiala = 100
    for tranz in newDelta:
        if isinstance(tranz, int):
            state = -tranz
            pass
        else:
            tranz[1] = -1 * tranz[1]
            if stare_initiala == 100:
                stare_initiala = state
            if state in delta:
                delta[state].append(tranz)
            else:
                Stari.append(state)
                delta[state] = [tranz]
                nr = nr + 1
    Findelta = {}
    finalStates = []
    for states in delta:
        for tranz in delta[states]:
            tranz[1] = findIN(Stari, tranz[1])
            caract = findIN(Stari, states)
            if caract in Findelta:
                Findelta[caract].append(tranz)
            else:
                okay = verificare(states, nfa.finalState)
                if okay == 1:
                    finalStates .append(caract)
                Findelta[caract] = [tranz]
    dfa = NFA(0, Findelta, finalStates, nr, nfa.alph)
    return dfa


def printare(dfa, out, nume):
    for x in dfa.alph:
        print(x, file=out, end="")
    print("", file=out)
    print(nume, file=out)
    print(dfa.initialState, file=out, end="")
    for state in dfa.delta:
        for tranz in dfa.delta[state]:
            print("", file=out)
            print(state, end=",", file=out)
            print("'" + tranz[0] + "'", end=",", file=out)
            print(tranz[1], file=out, end="")
    print("", file=out)
    if dfa.finalState == []:
        print("failed")
        print(0, file=out, end=" ")
    for state in dfa.finalState:
        print(state, file=out, end=" ")


def regex_dfa(input, output, nume):
    nfa = toafn(input)
    dfa = toDFN(nfa)
    printare(dfa, output, nume)


# part 2: Regex to Prenex form


def solutionare(cuv) -> str:
    lung = len(cuv)
    stivaOp = []
    x = 0
    while x < lung:
        if cuv[x] == "'":
            ghilim = cuv[x + 1:]
            str2 = "'"
            for elem in ghilim:
                str2 = str2 + elem
                if (elem == "'"):
                    break
            x = x + len(str2) - 1
            stivaOp.append(str2)
            pass
        elif cuv[x] == "|":
            strin = "UNION " + stivaOp.pop()
            stivaOp.append(strin)
        elif cuv[x] == "*":
            st = "STAR " + stivaOp.pop()
            stivaOp.append(st)
            pass
        elif cuv[x] == "+":
            st = "PLUS " + stivaOp.pop()
            stivaOp.append(st)
            pass
        else:
            if stivaOp == []:
                stivaOp.append(cuv[x])
            else:
                if cuv[x - 1] == "|":
                    stivaOp.append(cuv[x])
                    x = x + 1
                    continue
                strin = "CONCAT " + stivaOp.pop()
                stivaOp.append(strin)
                stivaOp.append(cuv[x])
        x = x + 1
    str1 = " "
    for elem in stivaOp:
        str1 = str1 + elem + " "
    str1 = str1[1:-1]
    return (str1)


def printareFisier(nume, str1, output, out2):
    with open(output, "w") as out:
        print(str1, file=out, end="")
    regex_dfa("auxunu", out2, nume)


def toprenex(input):
    ok = 0
    with open(input, "r") as input:
        with open("auxiliardoi", "w") as out2:
            line = input.read().splitlines()
            for regex in line:
                if ok == 1:
                    print("", file=out2)
                    print("", file=out2)
                ok = 1
                a = regex.split(" ", maxsplit=1)
                nume = a[0]
                cuv = a[1]

                stivaOp = []
                for x in range(10):
                    stivaOp.append([])
                nivel = 0
                asd = len(cuv) - 1
                x = 0
                while x < asd:
                    if cuv[x] == "(":
                        nivel = nivel + 1
                        x = x + 1
                        continue

                    elif cuv[x] == ")":
                        sol = solutionare(stivaOp[nivel])
                        stivaOp[nivel] = []
                        nivel = nivel - 1
                        x = x + 1
                        stivaOp[nivel].append(sol)
                        continue

                    stivaOp[nivel].append(cuv[x])
                    x = x + 1
                rezolvare = solutionare(stivaOp[0])
                printareFisier(nume, rezolvare, "auxunu", out2)


def runcompletelexer(Lexer, input, output):
    toprenex(Lexer)
    with open(output, "w") as out:
        print(Lexer, file=out)
    pass
    runlexer("auxiliardoi", input, output)


if __name__ == '__main__':
    lexer_file = "C:\\Users\\Cata\\Desktop\\Lexer_Pyton\\tests\\T3\\regex\\T3.5\\T3.5.lex"
    input_file = "C:\\Users\\Cata\\Desktop\\Lexer_Pyton\\tests\\T3\\regex\\T3.5\\input\\T3.5.8.in"
    output_file = "C:\\Users\\Cata\\Desktop\\Lexer_Pyton\\tests\\T3\\regex\\T3.10\\out\\eee.txt"
    print("Running...")
    runcompletelexer(lexer_file, input_file, output_file)
    print("Done!")
