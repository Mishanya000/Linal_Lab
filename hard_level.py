from typing import Union, List


class RingElement:
    """Базовый класс для элементов колец: целых чисел и полиномов."""

    def __init__(self, data: Union[int, List[float]]):
        """
        data:
        - если это целое число → элемент кольца Z;
        - если это список коэффициентов [a0, a1, ..., an] → полином a0 + a1*x + ... + an*x^n.
        """
        self.data = data
        self.is_polynomial = isinstance(data, list)

        if self.is_polynomial:
            while len(self.data) > 1 and abs(self.data[-1]) < 1e-10:  # удаление ведущих нулей для полиномов
                self.data.pop()

    def __repr__(self) -> str:
        """ Красивая отрисовка """
        if self.is_polynomial:
            terms = [f"{c}*x^{i}" if i > 0 else str(c) for i, c in enumerate(self.data) if c != 0]
            return " + ".join(terms) if terms else "0"
        return str(self.data)

    def degree(self):
        """ Возвращает степень полинома для полиномов, и 0 для свободных коэффициентов и целых чисел"""
        if self.is_polynomial: return len(self.data) - 1
        return 0

    def is_zero(self):
        """ Проверяет, является ли data нулём """
        if self.is_polynomial: return all(abs(c) < 1e-10 for c in self.data)
        return self.data == 0


def _gcd_two_integers(a: int, b: int) -> int:
    """ Вычисляет gcd двух целых чисел с помощью алгоритма Евклида
    Args:
        a, b - целые числа для поиска gcd
    Returns:
        НОД a и b
    """

    a, b = abs(a), abs(b)
    while b != 0:
        a, b = b, a % b
    return a


def _polynomial_division(dividend: List[float], divisor: List[float]):
    """ Выполняет деление полиномов с остатком.
    Args:
        dividend: коэффициенты делимого [a_0, a_1, ..., a_n]
        divisor: коэффициенты делителя [b_0, b_1, ..., b_m]

    Returns:
        кортеж из списков коэффициентов
    """
    dividend = [element for element in dividend]
    divisor = [element for element in divisor]

    while len(dividend) > 1 and abs(dividend[-1]) < 1e-10: dividend.pop()
    while len(divisor) > 1 and abs(divisor[-1]) < 1e-10: divisor.pop()

    if all(abs(c) < 1e-10 for c in divisor): raise ValueError("Ошибка деления на ноль")

    quotient = []

    while len(dividend) >= len(divisor):
        if all(abs(c) < 1e-10 for c in dividend):
            break

        coeff = dividend[-1] / divisor[-1]
        quotient.append(coeff)

        degree_diff = len(dividend) - len(divisor)
        for i in range(len(divisor)):
            dividend[degree_diff + i] -= coeff * divisor[i]

        dividend.pop()

    quotient.reverse()

    remainder = dividend if dividend else [0]
    quotient = quotient if quotient else [0]

    return quotient, remainder


def _gcd_two_polynomials(poly1: List[float], poly2: List[float]) -> List[float]:
    """ Вычисляет НОД двух полиномов с помощью алгоритма Евклида.
    Args:
        poly1, poly2: списки коэффициентов полиномов
    Returns:
        список коэффициентов НОД (нормализованный, старший коэффициент = 1)
    """
    a = [element for element in poly1]
    b = [element for element in poly2]

    while len(a) > 1 and abs(a[-1]) < 1e-10: a.pop()
    while len(b) > 1 and abs(b[-1]) < 1e-10: b.pop()

    while not all(abs(c) < 1e-10 for c in b):
        _, remainder = _polynomial_division(a, b)
        a, b = b, remainder

        while len(b) > 1 and abs(b[-1]) < 1e-10: b.pop()

    if a and abs(a[-1]) > 1e-10:  # сокращаю многочлен на старший коэффициент
        leading_coeff = a[-1]
        a = [c / leading_coeff for c in a]

    return a


def gcd_ring_elements(elements: List[RingElement]) -> RingElement:
    """
    Возвращает порождающий главного идеала, порождённого заданными элементами.
    - Для Z: НОД целых чисел.
    - Для K[x]: НОД полиномов (с коэффициентами в поле K).
    """

    if not elements: return RingElement(0)

    is_polynomial = elements[0].is_polynomial

    for elem in elements:
        if elem.is_polynomial != is_polynomial: raise ValueError("Все элементы должны быть одного типа")

    if is_polynomial:
        result = elements[0].data[:]
        for i in range(1, len(elements)):
            result = _gcd_two_polynomials(result, elements[i].data)
        return RingElement(result)
    else:
        result = abs(elements[0].data)
        for i in range(1, len(elements)):
            result = _gcd_two_integers(result, abs(elements[i].data))
        return RingElement(result)


def example_integers():
    """ Пример для целых чисел """
    print("Пример для целых чисел")

    numbers = [RingElement(48), RingElement(18), RingElement(30)]

    print("Образующие идеала:", [n.data for n in numbers])

    gcd = gcd_ring_elements(numbers)
    print(f"Порождающий элемент (НОД): {gcd.data}")

    # Проверяем принадлежность элемента идеалу
    test_element = 24
    belongs = (test_element % gcd.data == 0)
    print(f"Проверка: {test_element} принадлежит I?")
    print(f"Ответ: {'ДА' if belongs else 'НЕТ'} (т.к. {test_element} mod {gcd.data} = {test_element % gcd.data})")

    test_element = 25
    belongs = (test_element % gcd.data == 0)
    print(f"Проверка: {test_element} принадлежит I?")
    print(f"Ответ: {'ДА' if belongs else 'НЕТ'} (т.к. {test_element} mod {gcd.data} = {test_element % gcd.data})")
    print()


def example_polynomials():
    """ Пример работы с полиномами """
    print("Пример работы с полиномами")

    poly1 = RingElement([-1, 0, 1])  # x^2-1
    poly2 = RingElement([-1, 0, 0, 1])  # x^3-1

    polynomials = [poly1, poly2]

    print("Образующие идеала:")
    for p in polynomials:
        print(f"{p}")

    gcd = gcd_ring_elements(polynomials)
    print(f"Порождающий полином (НОД): {gcd}")

    test_poly = RingElement([0, 1, 1])  # x+x^2
    _, remainder = _polynomial_division(test_poly.data, gcd.data)
    belongs = all(abs(c) < 1e-10 for c in remainder)
    print(f"Проверка: {test_poly} принадлежит I?")
    print(f"Остаток от деления: {RingElement(remainder)}")
    print(f"Ответ: {'ДА' if belongs else 'НЕТ'}")
    test_poly_2 = RingElement([-1, 0, 1])
    _, remainder = _polynomial_division(test_poly_2.data, gcd.data)
    belongs = all(abs(c) < 1e-10 for c in remainder)
    print(f"Проверка {test_poly_2} принадлежит I?")
    print(f"Остаток от деления: {RingElement(remainder)}")
    print(f"Ответ: {'ДА' if belongs else "НЕТ"}")


example_integers()
example_polynomials()


"""
Как проверить принадлежность элемента идеалу
Элемент f принадлежит идеалу I = (d) тогда и только тогда, когда f делится на d без остатка:
-Для Z: проверяем f == 0 (mod d)
-Для K[x]: проверяем, что остаток от деления f на d равен 0
"""