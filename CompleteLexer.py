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


def processSimpleValue(operand) -> NFA:
    initialState = 0
    finalState = 1
    tranzitie = [operand, finalState]
    delta = [initialState, tranzitie]
    nfa = NFA(initialState, delta, finalState, finalState, [])
    return nfa


def processPlusOperation(operation) -> NFA:
    initialState = operation.finalState + 1
    finalState = operation.finalState + 2
    InitialEpsilonState = ["", operation.initialState]
    FinalEpsilonState = ["", finalState]
    delta = (
        operation.delta
        + [initialState, InitialEpsilonState]
        + [operation.finalState, InitialEpsilonState]
        + [operation.finalState, FinalEpsilonState]
    )
    nfa = NFA(initialState, delta, finalState, finalState, [])
    return nfa


def processStarOperation(operation) -> NFA:
    init_state = operation.finalState + 1
    finalState = operation.finalState + 2
    InitialEpsilonState = ["", operation.initialState]
    FinalEpsilonState = ["", finalState]
    delta = (
        operation.delta
        + [init_state, InitialEpsilonState]
        + [init_state, FinalEpsilonState]
        + [operation.finalState, InitialEpsilonState]
        + [operation.finalState, FinalEpsilonState]
    )
    nfa = NFA(init_state, delta, finalState, finalState, [])
    return nfa


def processUnionOperation(firstOperand, secondOperand) -> NFA:
    state = 0
    delta = []
    for transition in secondOperand.delta:
        if isinstance(transition, int):
            state = transition + firstOperand.finalState + 1
        else:
            transition[1] = transition[1] + firstOperand.finalState + 1
            delta = delta + [state, transition]
    InitialEpsilonState = ["", firstOperand.initialState]
    FinalEpsilonState = ["", secondOperand.initialState + firstOperand.finalState + 1]

    epsilon = [
        secondOperand.finalState + firstOperand.finalState + 2,
        InitialEpsilonState,
    ] + [secondOperand.finalState + firstOperand.finalState + 2, FinalEpsilonState]

    partialTransition = firstOperand.delta + delta + epsilon
    finalTransition = firstOperand.finalState + secondOperand.finalState + 1
    finalEpsilonTransition = [
        "",
        secondOperand.finalState + firstOperand.finalState + 3,
    ]
    epFinal = [finalTransition, finalEpsilonTransition] + [
        firstOperand.finalState,
        finalEpsilonTransition,
    ]

    TranzitiiFinale = partialTransition + epFinal
    stareFinala = secondOperand.finalState + firstOperand.finalState + 3
    stareInitiala = secondOperand.finalState + firstOperand.finalState + 2
    nfa = NFA(stareInitiala, TranzitiiFinale, stareFinala, stareFinala, [])
    return nfa


def procesConcatOperation(firstOperand, secondOperand) -> NFA:
    firstInitState = firstOperand.initialState
    secondInitState = secondOperand.initialState
    state = 0
    delta = []
    for transition in secondOperand.delta:
        if isinstance(transition, int):
            state = transition + firstOperand.finalState + 1
        else:
            position = transition[1] + firstOperand.finalState + 1
            deltaTranstition = [transition[0], position]
            delta = delta + [state, deltaTranstition]
    epsilonTransition = ["", secondInitState + firstOperand.finalState + 1]
    epsilon = [firstOperand.finalState, epsilonTransition]
    finalTransition = firstOperand.delta + delta + epsilon
    finalState = secondOperand.finalState + firstOperand.finalState + 1
    nfa = NFA(firstInitState, finalTransition, finalState, finalState, [])
    return nfa


def operationNumber(expresion) -> int:
    if expresion == "STAR":
        return 1
    if expresion == "PLUS":
        return 2

    if expresion == "CONCAT":
        return 3
    if expresion == "UNION":
        return 4
    if len(expresion) == 1:
        return 0
    return 60


def splitPhrase(phrase):
    splitUpPhrase = phrase.split(" ")
    elemList = []
    ok = 1
    for elem in splitUpPhrase:
        if (elem == "'") & (len(elem) == 1):
            if ok == 1:
                elem = "' '"
                ok = 0
            else:
                ok = 1
                continue
        elemList.append(elem)
    return elemList


def toAfn(input) -> NFA:
    with open(input, "r") as input:

        elemente = splitPhrase(input.readlines()[0])
        expresionStack = []
        stivaOperanzi = []
        alph = []
        for word in elemente:
            expresionStack.append(word)
            if len(word) == 1:
                if word not in alph:
                    alph.append(word)

            if word[0] == "'":
                alph.append(word[1:-1])
                expresionStack.pop()
                expresionStack.append(word[1:-1])

        while expresionStack:
            a = expresionStack.pop()
            if operationNumber(a) == 1:
                operand = stivaOperanzi.pop()
                star = processStarOperation(operand)
                stivaOperanzi.append(star)

            if operationNumber(a) == 2:
                operand = stivaOperanzi.pop()
                star = processPlusOperation(operand)
                stivaOperanzi.append(star)

            if operationNumber(a) == 3:
                firstOperand = stivaOperanzi.pop()
                secondOperand = stivaOperanzi.pop()
                concatenare = procesConcatOperation(firstOperand, secondOperand)
                stivaOperanzi.append(concatenare)

            if operationNumber(a) == 4:
                firstOperand = stivaOperanzi.pop()
                secondOperand = stivaOperanzi.pop()
                union = processUnionOperation(firstOperand, secondOperand)
                stivaOperanzi.append(union)

            if operationNumber(a) == 0:
                stivaOperanzi.append(processSimpleValue(a))

            if operationNumber(a) == 60:
                stivaOperanzi.append(processSimpleValue(a))

    deRet = stivaOperanzi.pop()
    deRet.alph = alph
    return deRet


# Using a Python dictionary to act as an adjacency list


def dfs(visited, graph, node):
    if node not in visited:
        visited.add(node)
        if node in graph.delta:
            for neighbour in graph.delta[node]:
                if neighbour[0] == "":
                    dfs(visited, graph, neighbour[1])


def step(lista, caracters, nfa, trans):
    ult = []
    for elem in lista:
        if elem in nfa.delta:
            for transition in nfa.delta[elem]:
                if caracters in transition:
                    var = transition[1]
                    ult = list(trans[var])
                    if ult == []:
                        return [var]
    return ult


def computeDelta(nfa, stare_actuala, visitedVector, newDelta):
    if stare_actuala == []:
        return newDelta
    for caracter in nfa.alph:
        stare_urm = step(stare_actuala, caracter, nfa, visitedVector)
        if stare_urm == []:
            tranzitie = [caracter, [99]]
            newDelta = newDelta + [stare_actuala, tranzitie]
        else:
            if True:
                shouldAdd = 1
                for i in range(len(newDelta)):
                    if newDelta[i] == stare_actuala:
                        if caracter in newDelta[i + 1]:
                            if newDelta[i + 1][1] == stare_urm:
                                tranzitie = [caracter, stare_urm]
                                newDelta = newDelta + [stare_actuala, tranzitie]
                                shouldAdd = 0
                if shouldAdd == 1:
                    tranzitie = [caracter, stare_urm]
                    newDelta = newDelta + [stare_actuala, tranzitie]
                    newDelta = computeDelta(nfa, stare_urm, visitedVector, newDelta)
    return newDelta


def epsilonClosure(nfa, visitetdVector, states):
    newDelta = []
    newDelta = computeDelta(
        nfa, list(visitetdVector[nfa.initialState]), visitetdVector, newDelta
    )
    for letter in nfa.alph:
        newDelta = newDelta + [[99], [letter, [99]]]
    delta = []
    for state in newDelta:
        isFound = 0
        for letter in nfa.alph:
            if letter in state:
                elementIdentifier = 0
                isFound = 1
                for element in state[1]:
                    elementIdentifier = elementIdentifier * 100 + element
                delta = delta + [startId, [state[0], elementIdentifier]]

        if isFound == 0:
            startId = 0
            for element in state:
                startId = startId * 100 + element
    return delta


def findPosition(lista, element):
    for x in range(len(lista)):
        if lista[x] == element:
            return x
    return -1


def matchStates(startingStates, finalStates):
    startingStates = startingStates * (-1)
    if startingStates == 0:
        if finalStates == 0:
            return True
        return False
    while startingStates > 0:
        if startingStates == finalStates:
            return True
        if startingStates % 100 == finalStates:
            return True
        else:
            startingStates = startingStates // 100
    return False


def toDFN(nfa) -> NFA:
    delta = {}
    for transition in nfa.delta:
        if isinstance(transition, int):
            state = transition
        else:
            if state in delta:
                delta[state].append(transition)
            else:
                delta[state] = [transition]

    nfa.delta = delta
    visitedVector = []
    for x in range(100):
        visitedVector.append([])

    for st in nfa.delta:
        visited = set()
        dfs(visited, nfa, st)
        visitedVector[st] = visited
    newDelta = epsilonClosure(nfa, visitedVector, [nfa.initialState])
    delta = {}
    Stari = []
    statesNumber = 0
    stare_initiala = 100
    for transition in newDelta:
        if isinstance(transition, int):
            state = -transition
        else:
            transition[1] = -1 * transition[1]
            if stare_initiala == 100:
                stare_initiala = state
            if state in delta:
                delta[state].append(transition)
            else:
                Stari.append(state)
                delta[state] = [transition]
                statesNumber = statesNumber + 1
    dfaDelta = {}
    finalStates = []
    for states in delta:
        for transition in delta[states]:
            transition[1] = findPosition(Stari, transition[1])
            caract = findPosition(Stari, states)
            if caract in dfaDelta:
                dfaDelta[caract].append(transition)
            else:
                if matchStates(states, nfa.finalState):
                    finalStates.append(caract)
                dfaDelta[caract] = [transition]
    dfa = NFA(0, dfaDelta, finalStates, statesNumber, nfa.alph)
    return dfa


def printare(dfa, out, nume):
    for letter in dfa.alph:
        print(letter, file=out, end="")
    print("", file=out)
    print(nume, file=out)
    print(dfa.initialState, file=out, end="")
    for state in dfa.delta:
        for transition in dfa.delta[state]:
            print("", file=out)
            print(state, end=",", file=out)
            print("'" + transition[0] + "'", end=",", file=out)
            print(transition[1], file=out, end="")
    print("", file=out)
    if dfa.finalState == []:
        print("failed")
        print(0, file=out, end=" ")
    for state in dfa.finalState:
        print(state, file=out, end=" ")


def regex_dfa(input, output, nume):
    nfa = toAfn(input)
    dfa = toDFN(nfa)
    printare(dfa, output, nume)


# part 2: Regex to Prenex form


def transformToPrenex(cuv) -> str:
    lungime = len(cuv)
    stivaOperanzi = []
    currentLength = 0
    while currentLength < lungime:
        if cuv[currentLength] == "'":
            textGhilimele = cuv[currentLength + 1 :]
            operand = "'"
            for elem in textGhilimele:
                operand = operand + elem
                if elem == "'":
                    break
            currentLength = currentLength + len(operand) - 1
            stivaOperanzi.append(operand)
        elif cuv[currentLength] == "|":
            union = "UNION " + stivaOperanzi.pop()
            stivaOperanzi.append(union)
        elif cuv[currentLength] == "*":
            star = "STAR " + stivaOperanzi.pop()
            stivaOperanzi.append(star)
        elif cuv[currentLength] == "+":
            plus = "PLUS " + stivaOperanzi.pop()
            stivaOperanzi.append(plus)
        else:
            if stivaOperanzi == []:
                stivaOperanzi.append(cuv[currentLength])
            else:
                if cuv[currentLength - 1] == "|":
                    stivaOperanzi.append(cuv[currentLength])
                    currentLength = currentLength + 1
                    continue
                concatenare = "CONCAT " + stivaOperanzi.pop()
                stivaOperanzi.append(concatenare)
                stivaOperanzi.append(cuv[currentLength])
        currentLength = currentLength + 1
    prenexText = " "
    for elem in stivaOperanzi:
        prenexText = prenexText + elem + " "
    prenexText = prenexText[1:-1]
    return prenexText


def printareFisier(nume, prenexForm, output, out2):
    with open(output, "w") as out:
        print(prenexForm, file=out, end="")
    regex_dfa("auxunu", out2, nume)


def toprenex(input):
    shouldPrint = False
    with open(input, "r") as input:
        with open("auxiliardoi", "w") as out2:
            line = input.read().splitlines()
            for regex in line:
                if shouldPrint:
                    print("", file=out2)
                    print("", file=out2)
                shouldPrint = True
                partionatedRegex = regex.split(" ", maxsplit=1)
                nume = partionatedRegex[0]
                word = partionatedRegex[1]

                stivaOperatii = []
                for currentCaracter in range(10):
                    stivaOperatii.append([])
                nivel = 0
                wordLength = len(word) - 1
                currentCaracter = 0
                while currentCaracter < wordLength:
                    if word[currentCaracter] == "(":
                        nivel = nivel + 1
                        currentCaracter = currentCaracter + 1
                        continue

                    elif word[currentCaracter] == ")":
                        newOperation = transformToPrenex(stivaOperatii[nivel])
                        stivaOperatii[nivel] = []
                        nivel = nivel - 1
                        currentCaracter = currentCaracter + 1
                        stivaOperatii[nivel].append(newOperation)
                        continue

                    stivaOperatii[nivel].append(word[currentCaracter])
                    currentCaracter = currentCaracter + 1
                penexForm = transformToPrenex(stivaOperatii[0])
                printareFisier(nume, penexForm, "auxunu", out2)


def runcompletelexer(Lexer, input, output):
    toprenex(Lexer)
    with open(output, "w") as out:
        print(Lexer, file=out)
    runlexer("auxiliardoi", input, output)


if __name__ == "__main__":
    lexer_file = "C:\\Users\\Cata\\Desktop\\git CV\\Lexer_Pyton\\tests\\T3\\regex\\T3.5\\T3.5.lex"
    input_file = "C:\\Users\\Cata\\Desktop\\git CV\\Lexer_Pyton\\tests\\T3\\regex\\T3.5\\input\\T3.5.8.in"
    output_file = "C:\\Users\\Cata\\Desktop\\eee.txt"
    print("Running...")
    runcompletelexer(lexer_file, input_file, output_file)
    print("Done!, check ", output_file)
