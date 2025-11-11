from typing import List, Dict, Tuple
from sympy import isprime, primefactors, gcd, totient
from math import factorial
import time


def simple_permutation(number: int) -> bool:
    """
    Проверяет, являются ли все циклические перестановки числа простыми числами.

    Parameters:
    number (int): Число для проверки

    Returns:
    bool: True если все циклические перестановки являются простыми числами, иначе False

    Example:
    simple_permutation(197)
    True  # потому что 197, 971, 719 все простые
    """
    string_number = str(number)
    count = 0
    list_perm = [int(string_number[i:] + string_number[:i]) for i in range(len(string_number))]
    for perm in list_perm:
        if isprime(perm):
            count += 1
    if count == len(list_perm):
        return True
    else:
        return False


def palindromic_squares_and_circular_primes() -> tuple[List[int], List[int]]:
    """
    Находит палиндромные числа и круговые простые числа в заданных диапазонах.

    Returns:
    tuple[List[int], List[int]]: Кортеж из двух списков:
        - Список палиндромных чисел до 10^5, которые остаются палиндромами при возведении в квадрат
        - Список круговых простых чисел до 10^6 (все циклические перестановки являются простыми)

    Note:
    Круговое простое число - это число, которое остается простым при любой циклической перестановке его цифр.
    """
    palindromic: List[int] = []
    for count in range(1, 10 ** 5):
        if count == int(str(count)[::-1]) and count ** 2 == int(str(count)[::-1]) ** 2:
            palindromic.append(count)
    permutations: List[int] = []
    for perm in range(1, 10 ** 6):
        if simple_permutation(perm):
            permutations.append(perm)
    return palindromic, permutations


def palindromic_cubes_and_palindromic_primes() -> tuple[List[int], List[int]]:
    """
    Находит палиндромные числа и палиндромные простые числа в заданных диапазонах.

    Returns:
    tuple[List[int], List[int]]: Кортеж из двух списков:
        - Список палиндромных чисел до 10^5, которые остаются палиндромами при возведении в куб
        - Список палиндромных простых чисел до 10000

    Note:
    Палиндромное простое число - это число, которое является и палиндромом, и простым числом.
    """
    palindromic: List[int] = []
    for count in range(1, 10 ** 5):
        if count == int(str(count)[::-1]) and count ** 3 == int(str(count)[::-1]) ** 3:
            palindromic.append(count)
    pal_primes: List[int] = []
    for prime in range(1, 10000):
        if prime == int(str(prime)[::-1]) and isprime(prime):
            pal_primes.append(prime)
    return palindromic, pal_primes


def primes_with_two_digits() -> Dict[str, List[int]]:
    """
    Генерирует простые числа, состоящие только из двух заданных цифр.

    Returns:
    Dict[str, List[int]]: Словарь, где ключи - строковые представления пар цифр,
                         значения - списки простых чисел, состоящих только из этих цифр

    Example:
    primes_with_two_digits()
    {'13': [13, 31, 113, 131, 311, ...], '15': [5, 151, ...], ...}

    Note:
    Использует поиск в ширину для генерации чисел из заданных цифр.
    """

    def generate_numbers(digits, limit=100):
        primes = []
        max_len = 20
        queue = [str(digits[0]), str(digits[1])]
        while queue and len(primes) < limit:
            num_str = queue.pop(0)
            num = int(num_str)
            if num > 1 and isprime(num):
                primes.append(num)
                if len(primes) == limit:
                    break
            if len(num_str) < max_len:
                for d in digits:
                    new_num_str = num_str + str(d)
                    queue.append(new_num_str)
        return primes

    digit_pairs = [(1, 3), (1, 5), (1, 7), (1, 9)]
    results = {}
    for pair in digit_pairs:
        results[f"1{str(pair[1])}"] = generate_numbers(pair, 100)
    print(results)
    return results


def twin_primes_analysis(limit_pairs: int = 1000) -> Tuple[List[Tuple[int, int]], List[float]]:
    """
    Анализ пар простых чисел-близнецов и отношения π₂(x)/π(x).

    Parameters:
    limit_pairs (int): Максимальное количество пар близнецов для нахождения (по умолчанию 1000)

    Returns:
    Tuple[List[Tuple[int, int]], List[float]]: Кортеж из:
        - Списка пар простых чисел-близнецов
        - Списка отношений π₂(x)/π(x) по мере нахождения пар

    Note:
    Простые числа-близнецы - это пары простых чисел, отличающихся на 2.
    π(x) - количество простых чисел ≤ x
    π₂(x) - количество пар простых чисел-близнецов ≤ x
    """
    num = 0
    pi = 0
    pi_2 = 0
    div_pi2pi = []
    list_limit_pairs = []
    while len(list_limit_pairs) < limit_pairs:
        num += 1
        if isprime(num):
            pi += 1
        if isprime(num) and isprime(num + 2):
            list_limit_pairs.append((num, num + 2))
            div_pi2pi.append(pi_2 / pi)
            pi_2 += 1
    print(list_limit_pairs)
    print(div_pi2pi)
    return list_limit_pairs, div_pi2pi


def factorial_plus_one_factors() -> Dict[int, Dict[int, int]]:
    """
    Факторизация чисел вида n! + 1 для n от 2 до 50.

    Returns:
    Dict[int, Dict[int, int]]: Словарь, где:
        - Ключи: значения n от 2 до 50
        - Значения: словари с разложением на простые множители, где:
            - Ключи: простые множители
            - Значения: их степени

    Example:
    factorial_plus_one_factors()
    {2: {3: 1}, 3: {7: 1}, 4: {5: 2}, ...}

    Note:
    Исследует числа n! + 1, которые часто являются простыми для небольших n
    (известные как факториальные простые числа).
    """
    primefactors_list = []
    num_big_prime_digit = {}
    dict_for_numbers = {}
    for num in range(2, 51):
        dict_for_number = {}
        number = factorial(num) + 1
        #        primefactors_list.append(len(primefactors(number)))
        list_prime = primefactors(number)
        # for j in list_prime:
        #     if j > 10 ** 6:
        #         num_big_prime_digit[num] = j
        for i in list_prime:
            dict_for_number[i] = list_prime.count(i)
        dict_for_numbers[num] = dict_for_number
    print(dict_for_numbers)
    print(num_big_prime_digit)
    return dict_for_numbers


def euler_phi_direct(n: int) -> int:
    """
    Вычисляет функцию Эйлера φ(n) прямым методом.

    Parameters:
    n (int): Натуральное число

    Returns:
    int: Количество чисел от 1 до n, взаимно простых с n

    Note:
    Прямой метод перебирает все числа от 1 до n и проверяет НОД с n.
    Эффективен для небольших n.
    """
    count = 0
    if n <= 0:
        return 0
    for num in range(1, n + 1):
        if gcd(num, n) == 1:
            count += 1
    print(count)
    return count


def euler_phi_factor(n: int) -> int:
    """
    Вычисляет функцию Эйлера φ(n) через разложение на простые множители.

    Parameters:
    n (int): Натуральное число

    Returns:
    int: Количество чисел от 1 до n, взаимно простых с n

    Formula:
    φ(n) = n × ∏(1 - 1/p) для всех различных простых делителей p числа n

    Note:
    Этот метод более эффективен для больших чисел, если известно разложение на множители.
    """
    primefactors_n = primefactors(n)
    phi = n
    for prime in primefactors_n:
        phi = int(phi * (1 - 1 / prime))
    print(phi)
    return phi


def compare_euler_phi_methods(test_values: List[int]) -> dict:
    """
    Сравнивает производительность различных методов вычисления функции Эйлера.

    Parameters:
    test_values (List[int]): Список чисел для тестирования

    Returns:
    dict: Словарь с результатами сравнения времени выполнения:
        - Ключи: тестовые числа
        - Значения: словари с временем выполнения для каждого метода

    Methods:
    - 'direct': Прямой перебор (euler_phi_direct)
    - 'factor': Через разложение на множители (euler_phi_factor)
    - 'sympy': Встроенная функция из SymPy (totient)

    Note:
    Полезно для выбора оптимального метода вычисления в зависимости от размера числа.
    """
    time_results = {}
    for test_value in test_values:
        method_times = {}

        start_time1 = time.perf_counter()
        res1 = euler_phi_direct(test_value)
        time1 = time.perf_counter() - start_time1
        method_times['direct'] = time1

        start_time2 = time.perf_counter()
        res2 = euler_phi_factor(test_value)
        time2 = time.perf_counter() - start_time2
        method_times['factor'] = time2

        start_time3 = time.perf_counter()
        res3 = totient(test_value)
        time3 = time.perf_counter() - start_time3
        method_times['sympy'] = time3

        time_results[test_value] = {'times': method_times}
    print(time_results)
    return time_results


compare_euler_phi_methods([1000, 15, 89])
