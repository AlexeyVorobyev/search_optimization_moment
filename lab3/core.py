import random


def getFunc1():
    def mathFunc1(x, y):
        return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2

    return [mathFunc1, (-5,5 ), (-5, 5)]


def generateFirstPopulation(targetFunc, populationSize):
    limitsX = targetFunc[1]
    limitsY = targetFunc[2]
    # шанс мутации
    result = Population(0.2)

    randXs = [random.uniform(*limitsX) for _ in range(populationSize)]
    randYs = [random.uniform(*limitsY) for _ in range(populationSize)]

    for randX, randY in zip(randXs, randYs):
        result.add_species(
            Species.from_floats((randX, randY), min(limitsX[0], limitsY[0]), max(limitsX[1], limitsY[1])))

    print(f'[DEBUG] First population:')
    for species in result.species:
        print(f'[DEBUG] * {species.to_floats()}')
    return result


def trigger():
    scoringFunction = getFunc1()[0]
    # Размер популяции
    population = generateFirstPopulation(getFunc1(), 5000)
    # Количество поколений
    generationsCount = 20

    result = []

    for i in range(generationsCount - 1):
        bestSpecies = population.bestSpecies(scoringFunction).to_floats()
        result.append({
            "generation": i,
            "data": bestSpecies,
            "fitness": getFunc1()[0](*bestSpecies)
        })
        print(f'Best in generation {i + 1}: {bestSpecies}; fitness: {getFunc1()[0](*bestSpecies)}')
        population.reproduce(scoringFunction)

    bestSpecies = population.bestSpecies(scoringFunction).to_floats()
    print(f'Last generation best: {bestSpecies}; fitness: {getFunc1()[0](*bestSpecies)}')
    result.append({
        "generation": generationsCount,
        "data": bestSpecies,
        "fitness": getFunc1()[0](*bestSpecies)
    })

    return result


class Population:
    def __init__(self, mutationChance):
        self.species = []
        self.mutationChance = mutationChance

    def add_species(self, species):
        self.species.append(species)

    # Произвести размножение. В результате - замена особей этой популяции на новые
    def reproduce(self, scoringFunction, resultSpeciesCount=None):
        if (resultSpeciesCount is None):
            resultSpeciesCount = len(self.species)

        children = self.crossingover()
        self.mutate(children)
        # for child in children:
        #     print(f'[DEBUG] {child.bits}')
        contestants = self.species + children
        scores = {}
        for contestant in contestants:
            scores[contestant] = scoringFunction(*contestant.to_floats())



        self.species = sorted(scores, key=scores.get)[:resultSpeciesCount]

    def bestSpecies(self, scoringFunction):
        scores = {}
        for speciesSubject in self.species:
            scores[speciesSubject] = scoringFunction(*speciesSubject.to_floats())

        return min(scores, key=scores.get)

    # Произвести скрещивание. Формируем брачные пары и обменяемся участками особей.
    # Возвращает список получившихся детей
    def crossingover(self):
        children = []
        pairs = {}
        for speciesSubject in self.species:
            pairs[speciesSubject] = random.choice(self.species)

        for parent1, parent2 in pairs.items():
            chromos1 = parent1.bits
            chromos2 = parent2.bits
            breakPoint = random.randrange(1, len(chromos1[0]))
            resultChromos = []

            for coordIdx in range(len(chromos1)):
                bitsList1 = chromos1[coordIdx]
                bitsList2 = chromos2[coordIdx]
                resultBitsList1 = bitsList1[0:breakPoint] + bitsList2[breakPoint:]
                resultBitsList2 = bitsList2[0:breakPoint] + bitsList1[breakPoint:]
                resultChromos.append((resultBitsList1, resultBitsList2))

            for coordIdx in range(len(chromos1)):
                speciesCromos = []
                for resultChromo in resultChromos:
                    speciesCromos.append(resultChromo[coordIdx])
                children.append(Species(speciesCromos, min(parent1.encodingFrom, parent2.encodingFrom),
                                        max(parent1.encodingTo, parent2.encodingTo)))

        return children

    def mutate(self, species):
        for speciesSubject in species:
            if random.uniform(0, 1) < self.mutationChance:
                changingBitNumber = random.randrange(0, len(speciesSubject.bits[0]))
                # print(f'MuTaTiOn! changing bit: {changingBitNumber}')
                # print(f'BEFORE: {speciesSubject.bits}')

                coordinateIdx = random.randrange(0, len(speciesSubject.bits))
                speciesSubject.bits[coordinateIdx][changingBitNumber] = 1 - speciesSubject.bits[coordinateIdx][
                    changingBitNumber]
                # print(f'AFTER:  {speciesSubject.bits}')


class Species:
    # Точность знака
    ENCODING_PRECISION = 100

    # Конструктор из массива вещественных чисел
    def from_floats(floatsValues, encodingFrom, encodingTo):
        # Если передан не список, оборачиваем в список
        if (type(floatsValues) is not list) and (type(floatsValues) is not tuple):
            floatsValues = [floatsValues]

        bitsStrings = []
        for floatValue in floatsValues:
            encoded_int = round(
                (floatValue - encodingFrom) * (2 ** Species.ENCODING_PRECISION - 1) / (encodingTo - encodingFrom))
            binString = "{0:b}".format(encoded_int)
            bitsStrings.append(('0' * (Species.ENCODING_PRECISION - len(binString))) + binString)
        return Species(bitsStrings, encodingFrom, encodingTo)

    def __init__(self, bitsStrings, encodingFrom, encodingTo):
        self.encodingFrom = encodingFrom
        self.encodingTo = encodingTo
        # Если передан не список, оборачиваем в список
        if (type(bitsStrings) is not list) and (type(bitsStrings) is not tuple):
            bitsStrings = [bitsStrings]

        self.bits = [[int(x) for x in bitsString] for bitsString in bitsStrings]

    def to_floats(self):
        result = []
        for bitsList in self.bits:
            bitsString = ''.join(map(str, bitsList))
            encoded_int = int(bitsString, base=2)
            floatValue = (encoded_int * (self.encodingTo - self.encodingFrom)) / (
                    2 ** Species.ENCODING_PRECISION - 1) + self.encodingFrom
            result.append(floatValue)
        return result
