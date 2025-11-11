import random
from typing import Dict, List, Tuple, Union
from sympy.combinatorics import SymmetricGroup, Permutation, PermutationGroup
from sympy import factorial, gcd
from itertools import product
from galois import GF, Poly


def subgroups_of_Sm(N: int) -> Dict:
    """
    Анализ подгрупп симметрической группы S_m.

    Для заданного N вычисляет m = 4 + N % 5 и возвращает информацию о подгруппах S_m:
    - Общее количество подгрупп (предварительно вычисленные значения)
    - Случайную циклическую подгруппу
    - Индекс выбранной подгруппы
    - Является ли выбранная подгруппа нормальной

    Parameters:
    N (int): Входной параметр для вариативности вычислений

    Returns:
    Dict: Словарь с информацией о подгруппах
    """
    m = 4 + N % 5

    group = SymmetricGroup(m)
    group_elements = group.elements
    subgroup_counts = {4: 30, 5: 156, 6: 1455, 7: 11300, 8: 151221}
    count_subgroups = subgroup_counts[m]

    cyclic_subgroups_set = set()
    for g in group_elements:
        cyclic_subgroup = group.subgroup([g])
        subgroup_elements_tuple = tuple(sorted(cyclic_subgroup.elements, key=str))
        cyclic_subgroups_set.add(subgroup_elements_tuple)

    cyclic_subgroups = []
    for elements_tuple in cyclic_subgroups_set:
        subgroup = PermutationGroup(elements_tuple)
        cyclic_subgroups.append(subgroup)

    random_subgroup = random.choice(cyclic_subgroups)

    subgroup_for_cosets = cyclic_subgroups[N % count_subgroups]
    subgroup_elements = set(subgroup_for_cosets.generate())
    left_cosets = set()
    right_cosets = set()

    for g in group_elements:
        left_coset = frozenset(g * h for h in subgroup_elements)
        right_coset = frozenset(h * g for h in subgroup_elements)
        left_cosets.add(left_coset)
        right_cosets.add(right_coset)

    is_normal = (sorted(left_cosets) == sorted(right_cosets))

    result = dict()
    result['Кол_во подгрупп'] = count_subgroups
    result['Случайная подгруппа'] = list(random_subgroup.generate())
    result[f'Индекс {list(subgroup_for_cosets.generate())}'] = len(left_cosets)
    result['Нормальная'] = is_normal
    return result


def element_powers_in_Sm(N: int) -> Dict:
    """
    Анализ степеней элементов и порожденных ими подгрупп в симметрической группе.

    Для заданного N вычисляет m = 4 + N % 5 и выбирает элемент из S_m.
    Исследует степени этого элемента и циклические подгруппы, порожденные этими степенями.

    Parameters:
    N (int): Входной параметр для вариативности вычислений

    Returns:
    Dict: Словарь с информацией о степенях элемента и порожденных подгруппах
    """
    m = 4 + N % 5
    n1 = N % 6
    n2 = (N + 1) % 6
    n3 = (N + 2) % 6

    group = SymmetricGroup(m)
    group_elements = list(group.generate())

    element = group_elements[N % factorial(m)]
    element_n1 = element ** n1
    element_n2 = element ** n2
    element_n3 = element ** n3

    group_n1 = group.subgroup([element_n1])
    group_n2 = group.subgroup([element_n2])
    group_n3 = group.subgroup([element_n3])

    orders = dict()
    orders['g'] = element
    orders['o(g_n1)'] = [element_n1, element_n1.order()]
    orders['o(g_n2)'] = [element_n2, element_n2.order()]
    orders['o(g_n3)'] = [element_n3, element_n3.order()]
    orders['|<g_n1>|'] = [str(group_n1), group_n1.order()]
    orders['|<g_n2>|'] = [str(group_n2), group_n2.order()]
    orders['|<g_n3>|'] = [str(group_n3), group_n3.order()]
    return orders


def solve_sigma_power_eq(N: int) -> Dict:
    """
    Решение уравнения вида σ^n = τ в симметрической группе.

    Находит все перестановки σ в S_m такие, что некоторая степень σ равна
    фиксированной перестановке τ. Возвращает количество решений и примеры.

    Parameters:
    N (int): Входной параметр для вариативности вычислений

    Returns:
    Dict: Словарь с количеством решений и примерами
    """
    m = 4 + N % 5

    group = SymmetricGroup(m)
    group_elements = list(group.generate())

    solutions = set()
    answer = list(range(1, m))
    answer.append(0)
    for element in group_elements:
        for n in range(element.order()):
            if element ** n == Permutation(answer):
                solutions.add(element)

    result = dict()
    result['Кол-во решений'] = len(solutions)
    result['3 случайных решения'] = [random.choice(list(solutions)) for _ in range(3)]
    return result


def elements_of_order_k_in_cyclic_group(N: int) -> Dict:
    """
    Поиск элементов заданного порядка в симметрической группе.

    Для заданного N вычисляет m = 4 + N % 5 и k = 1 + N % 7.
    Находит все элементы, удовлетворяющие условию g^k = e, и все элементы порядка k.

    Parameters:
    N (int): Входной параметр для вариативности вычислений

    Returns:
    Dict: Словарь с двумя списками элементов
    """
    m = 4 + N % 5
    k = 1 + N % 7

    group = SymmetricGroup(m)
    group_elements = list(group.generate())

    list_power = list()
    list_orders = list()
    for element in group_elements:
        if element ** k == Permutation(range(m)):
            list_power.append(element)
        if element.order() == k:
            list_orders.append(element)

    result = dict()
    result['Список g ** k = e'] = list_power
    result['Список o(g) = k'] = list_orders
    return result


def subgroups_of_Zm_star(N: int) -> List[List[int]]:
    """
    Нахождение всех подгрупп мультипликативной группы вычетов по модулю m.

    Для заданного N вычисляет m = 4 + N % 5 и строит все циклические подгруппы
    мультипликативной группы Z_m^*.

    Parameters:
    N (int): Входной параметр для вариативности вычислений

    Returns:
    List[List[int]]: Отсортированный список подгрупп
    """
    m = 4 + N % 5
    units = [a for a in range(1, m) if gcd(a, m) == 1]
    subgroups_set = set()
    subgroups_set.add(tuple([1]))
    for g in units:
        subgroup = []
        x = g
        while x not in subgroup:
            subgroup.append(x)
            x = (x * g) % m
        subgroup_tuple = tuple(sorted(subgroup))
        subgroups_set.add(subgroup_tuple)
    result = [list(t) for t in subgroups_set]
    result.sort(key=lambda x: (len(x), x))
    return result


def order_of_sr(N: int) -> int:
    """
    Вычисление порядка элемента в мультипликативной группе простого поля.

    Для фиксированного простого числа p = 31 вычисляет порядок элемента s^r
    в мультипликативной группе F_p^*.

    Parameters:
    N (int): Входной параметр (используется для выбора конкретного случая)

    Returns:
    int: Порядок элемента s^r
    """
    p = 0
    if N == 1:
        p = 31
    s = 4  # тк N = 1
    r = 60  # N = 1
    temp = s % p
    m = 1
    while temp != 1:
        temp = (temp * s) % p
        m += 1

    gcd_ord = gcd(m, r)
    return m // gcd_ord


def order_and_primitivity_of_t(N: int) -> Dict[int, str]:
    """
    Проверка, является ли элемент примитивным в мультипликативной группе поля.

    Для фиксированного простого числа p = 31 вычисляет порядок элемента t
    и проверяет, является ли он примитивным (порождающим) элементом.

    Parameters:
    N (int): Входной параметр (используется для выбора конкретного случая)

    Returns:
    Dict[int, str]: Словарь с порядком и ответом YES/NO
    """
    p = 0
    if N == 1:
        p = 31
    t = 8
    m = 1
    temp = t % p
    while temp != 1:
        temp = (temp * t) % p
        m += 1
    if m == p - 1:
        return {m: 'YES'}
    else:
        return {m: 'NO'}


def generators_of_Zm_star(N: int) -> List[int]:
    """
    Поиск всех примитивных элементов мультипликативной группы вычетов.

    Для заданного N вычисляет m = 4 + N % 5 и находит все элементы,
    порождающие мультипликативную группу Z_m^*.

    Parameters:
    N (int): Входной параметр для вариативности вычислений

    Returns:
    List[int]: Список примитивных элементов
    """
    elem_list = []
    m = 4 + N % 5
    group_order = m - 1
    for elem in range(1, m):
        el_ord = 1
        temp = elem % m
        while temp != 1:
            temp = (temp * elem) % m
            el_ord += 1
        if el_ord == group_order:
            elem_list.append(elem)
    return elem_list


def cyclic_subgroup_in_Zm_additive(N: int) -> Dict[int, List[int]]:
    """
    Анализ циклической подгруппы в аддитивной группе вычетов.

    Для заданного N вычисляет m = 4 + N % 5 и строит циклическую подгруппу,
    порожденную элементом t = 8 mod m. Находит примитивные элементы этой подгруппы.

    Parameters:
    N (int): Входной параметр для вариативности вычислений

    Returns:
    Dict[int, List[int]]: Словарь с порядком подгруппы и списком примитивных элементов
    """
    m = 4 + N % 5
    t_base = 8
    t = t_base % m
    subgroup = set()
    for i in range(m):
        subgroup.add((t * i) % m)
    subgroup_order = len(subgroup)
    primitive_elements = []
    for elem in subgroup:
        if elem == 0:
            continue
        if m // gcd(m, elem) == subgroup_order:
            primitive_elements.append(elem)
    return {subgroup_order: primitive_elements}


def isomorphism_of_cyclic_subgroup_Zm_star(N: int) -> Dict[int, Tuple[set, str]]:
    """
    Установление изоморфизма между циклической подгруппой и подгруппой симметрической группы.

    Для заданного N вычисляет m = 4 + N % 5, строит циклическую подгруппу
    и устанавливает ее изоморфизм с циклической подгруппой в S_d.

    Parameters:
    N (int): Входной параметр для вариативности вычислений

    Returns:
    Dict[int, Tuple[set, str]]: Словарь с порядком подгруппы и информацией об изоморфизме
    """
    m = 4 + N % 5
    t_old = 8
    t = t_old % m
    subgroup = set()
    for i in range(1, m):
        subgroup.add((i * t) % m)
    d = len(subgroup)
    cyclic_group = f"<(1 2 ... {d})> при S{d}"
    return {d: (subgroup, cyclic_group)}


def ai(N: int, i: int) -> int:
    return (i + N) % 4


def bj(N: int, j: int) -> int:
    return (j + N) % 7


def ck(N: int, k: int) -> int:
    return (k + N) % 5


def dl(N: int, l: int) -> int:
    return (l + N) % 9


def rm(N: int, m: int) -> int:
    return (m + N) % 11


def st(N: int, t: int) -> int:
    return (t + N) % 11


def roots_F4(N: int) -> List[str]:
    """
    Нахождение корней полинома над полем F4.

    Строит полином степени 8 с коэффициентами, зависящими от N,
    и находит все его корни в поле F4.

    Parameters:
    N (int): Входной параметр для вариативности вычислений

    Returns:
    List[str]: Список корней полинома в строковом представлении
    """
    field = GF(4)
    coefficients = [field(1)] + [field(ai(N, i)) for i in range(8, -1, -1)]
    func = Poly(coefficients, field=field)
    roots = [str(root) for root in func.roots()]
    return roots


def roots_F7(N: int) -> List[str]:
    """
    Нахождение корней полинома над полем F7.

    Строит полином степени 6 с коэффициентами, зависящими от N,
    и находит все его корни в поле F7.

    Parameters:
    N (int): Входной параметр для вариативности вычислений

    Returns:
    List[str]: Список корней полинома в строковом представлении
    """
    field = GF(7)
    coefficients = [field(bj(N, i)) for i in range(6, -1, -1)]
    func = Poly(coefficients, field=field)
    roots = [str(root) for root in func.roots()]
    return roots


def reducibility_F5(N: int) -> str:
    """
    Разложение полинома на неприводимые множители над полем F5.

    Строит полином степени 5 с коэффициентами, зависящими от N,
    и разлагает его на неприводимые множители над полем F5.

    Parameters:
    N (int): Входной параметр для вариативности вычислений

    Returns:
    str: Строка с разложением полинома на множители
    """
    field = GF(5)
    coefficients = [field(1)] + [field((ck(N, i))) for i in range(4, -1, -1)]
    func = Poly(coefficients, field=field)
    factors = func.factors()

    result = 'f(x) ='
    for factor, power in zip(factors[0], factors[1]):
        result += f' ({factor})^{power} *'
    return result[:-2]


def reducibility_F9(N: int) -> str:
    """
    Разложение полинома на неприводимые множители над полем F9.

    Строит полином степени 4 с коэффициентами, зависящими от N,
    и разлагает его на неприводимые множители над полем F9.

    Parameters:
    N (int): Входной параметр для вариативности вычислений

    Returns:
    str: Строка с разложением полинома на множители
    """
    field = GF(9)
    coefficients = [field(1)] + [field((dl(N, i))) for i in range(3, -1, -1)]
    func = Poly(coefficients, field=field)
    factors = func.factors()

    result = 'f(x) ='
    for factor, power in zip(factors[0], factors[1]):
        result += f' ({factor})^{power} +'
    return result[:-2]


def gcd_F11(N: int) -> str:
    """
    Нахождение НОД двух полиномов и его линейного представления над полем F11.

    Использует расширенный алгоритм Евклида для нахождения НОД двух полиномов
    и его представления в виде линейной комбинации исходных полиномов.

    Parameters:
    N (int): Входной параметр для вариативности вычислений

    Returns:
    str: Строка с линейным представлением НОД
    """
    field = GF(11)
    coefficients_f = [field((rm(N, i))) for i in range(7, -1, -1)]
    coefficients_g = [field((st(N, i))) for i in range(3, -1, -1)]
    func_f = Poly(coefficients_f, field=field)
    func_g = Poly(coefficients_g, field=field)

    table1 = [func_f, field(1), field(0)]
    table2 = [func_g, field(0), field(1)]
    while table1[0] != field(0) and table2[0] != field(0):
        if table1[0].degree > table2[0].degree:
            coef_to_multiply = [1] + [0 for _ in range(table1[0].degree - table2[0].degree)]
            table1[0] -= table2[0] * Poly(coef_to_multiply, field=field)
            table1[1] -= table2[1] * Poly(coef_to_multiply, field=field)
            table1[2] -= table2[2] * Poly(coef_to_multiply, field=field)
        elif table1[0].degree < table2[0].degree:
            coef_to_multiply = [1] + [0 for _ in range(table2[0].degree - table1[0].degree)]
            table2[0] -= table1[0] * Poly(coef_to_multiply, field=field)
            table2[1] -= table1[1] * Poly(coef_to_multiply, field=field)
            table2[2] -= table1[2] * Poly(coef_to_multiply, field=field)
        else:
            if table1[0].coeffs[0] >= table2[0].coeffs[0]:
                table1[0] -= table2[0]
                table1[1] -= table2[1]
                table1[2] -= table2[2]
            else:
                table2[0] -= table1[0]
                table2[1] -= table1[1]
                table2[2] -= table1[2]

    if table1[0] == field(0):
        return f'{table2[0]} = ({func_f}) * ({table2[1]}) + ({func_g}) * ({table2[2]})'
    else:
        return f'{table1[0]} = ({func_f}) * ({table1[1]}) + ({func_g} * {table1[2]})'


def inverse_F13(N: int) -> Union[str, Tuple[str, str]]:
    """
    Нахождение обратного полинома по модулю заданного полинома над полем F13.

    Использует расширенный алгоритм Евклида для нахождения обратного элемента
    полинома f(x) в кольце полиномов по модулю g(x).

    Parameters:
    N (int): Входной параметр для вариативности вычислений

    Returns:
    Union[str, Tuple[str, str]]: Результат поиска обратного элемента или сообщение о необратимости
    """
    field = GF(13)
    coefficients_f = [field((st(N, i))) for i in range(3, -1, -1)]
    coefficients_g = [1, 0, 0, 0, 1, 1, 0, 6, 2]
    func_f = Poly(coefficients_f, field=field)
    func_g = Poly(coefficients_g, field=field)

    table1 = [func_f, field(1), field(0)]
    table2 = [func_g, field(0), field(1)]
    while table1[0] != field(0) and table2[0] != field(0):
        if table1[0].degree > table2[0].degree:
            coef_to_multiply = [1] + [0 for _ in range(table1[0].degree - table2[0].degree)]
            table1[0] -= table2[0] * Poly(coef_to_multiply, field=field)
            table1[1] -= table2[1] * Poly(coef_to_multiply, field=field)
            table1[2] -= table2[2] * Poly(coef_to_multiply, field=field)
        elif table1[0].degree < table2[0].degree:
            coef_to_multiply = [1] + [0 for _ in range(table2[0].degree - table1[0].degree)]
            table2[0] -= table1[0] * Poly(coef_to_multiply, field=field)
            table2[1] -= table1[1] * Poly(coef_to_multiply, field=field)
            table2[2] -= table1[2] * Poly(coef_to_multiply, field=field)
        else:
            if table1[0].coeffs[0] >= table2[0].coeffs[0]:
                table1[0] -= table2[0]
                table1[1] -= table2[1]
                table1[2] -= table2[2]
            else:
                table2[0] -= table1[0]
                table2[1] -= table1[1]
                table2[2] -= table1[2]

    if table1[0] == field(0):
        if table2[0].degree != 0:
            return 'необратим'
        func_h = table2[1] // table2[0]
    else:
        if table1[0].degree != 0:
            return 'необратим'
        func_h = table1[1] // table1[0]

    return f'({func_h}) * ({func_f}) ≡ 1 mod ({func_g})', f'h(x) = {func_h}'


def generate_irreducible_polynomials(q: int, d: int) -> List[str]:
    """
    Генерация всех неприводимых полиномов заданной степени над конечным полем.

    Перебирает все монтические полиномы степени d над полем F_q
    и проверяет их на неприводимость.

    Parameters:
    q (int): Характеристика поля
    d (int): Степень полиномов

    Returns:
    List[str]: Список неприводимых полиномов в строковом представлении
    """
    field = GF(q)
    irreducibles = []

    for part_coefs in product([field(i) for i in range(q)], repeat=d):
        coefficients = [field(1)] + list(part_coefs)
        func_f = Poly(coefficients, field=field)
        reducible = False
        for deg_g in range(1, d // 2 + 1):
            for coefs_g in product([field(i) for i in range(q)], repeat=deg_g):
                g = Poly([field(1)] + list(coefs_g), field=field)
                if func_f % g == 0:
                    reducible = True
                    break
            if reducible:
                break

        if not reducible:
            irreducibles.append(str(func_f))

    return irreducibles


ISU = 502701
N = ISU % 20