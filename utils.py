"""
Вспомогательные функции: парсинг математических выражений
"""

import numpy as np
from sympy import symbols, sympify, lambdify, sin, cos, tan, asin, acos, atan, sinh, cosh, tanh, exp, log, sqrt, pi


def parse_expression(expr_str, variables, custom_vars=None):
    """Парсит строку с математическим выражением"""
    syms = symbols(variables)

    available_functions = {
        'sin': sin, 'cos': cos, 'tan': tan,
        'asin': asin, 'acos': acos, 'atan': atan,
        'sinh': sinh, 'cosh': cosh, 'tanh': tanh,
        'exp': exp, 'log': log, 'log10': lambda x: log(x, 10),
        'sqrt': sqrt,
        'pi': pi, 'e': exp(1),
        'abs': abs
    }

    if custom_vars:
        available_functions.update(custom_vars)

    try:
        expr = sympify(expr_str, locals=available_functions, evaluate=False)
        f = lambdify(syms, expr, modules='numpy')
        return f
    except Exception as e:
        raise ValueError(f"Ошибка парсинга выражения '{expr_str}': {str(e)}")


def make_function_with_coeffs(expr_str, variables, coeff_dict):
    """Создаёт функцию с подстановкой коэффициентов"""
    if not expr_str or expr_str.strip() == '':
        return None

    expr_processed = expr_str
    for coeff_name, coeff_val in coeff_dict.items():
        expr_processed = expr_processed.replace(coeff_name, str(coeff_val))

    f = parse_expression(expr_processed, variables, {})

    def func(*args):
        result = f(*args)
        if isinstance(result, np.ndarray):
            if result.size == 1:
                return float(result[0])
            return result
        return result

    return func