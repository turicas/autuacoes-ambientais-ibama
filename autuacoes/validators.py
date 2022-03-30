import re


INVALID_CPFS = tuple(str(i) * 11 for i in range(10))
CNPJ_MULTIPLIERS_1 = tuple(int(x) for x in "543298765432")
CNPJ_MULTIPLIERS_2 = tuple(int(x) for x in "6543298765432")
REGEXP_NUMBERS = re.compile("[0-9]")


def cpf_checks(text):
    """
    >>> cpf_checks("111111111xx")
    '11'

    >>> cpf_checks("123456789xx")
    '09'
    """
    check_1 = str(((sum(int(c) * (10 - i) for i, c in enumerate(text[:9])) * 10) % 11) % 10)
    check_2 = str(((sum(int(c) * (11 - i) for i, c in enumerate(text[:9] + check_1)) * 10) % 11) % 10)
    return check_1 + check_2


def is_valid_cpf(text):
    text = "".join(REGEXP_NUMBERS.findall(text)).strip()
    if not text.isdigit() or len(text) > 11:
        return False
    text = "0" * (11 - len(text)) + text
    if text in INVALID_CPFS:
        return False
    return cpf_checks(text) == text[-2:]


def cnpj_checks(text):
    check_1 = sum(int(c) * m for c, m in zip(text[:12], CNPJ_MULTIPLIERS_1)) % 11
    check_1 = str(11 - check_1 if check_1 >= 2 else 0)
    check_2 = sum(int(c) * m for c, m in zip(text[:12] + check_1, CNPJ_MULTIPLIERS_2)) % 11
    check_2 = str(11 - check_2 if check_2 >= 2 else 0)
    return check_1 + check_2


def is_valid_cnpj(text):
    text = "".join(REGEXP_NUMBERS.findall(text)).strip()
    if not text.isdigit() or len(text) > 14:
        return False
    text = "0" * (14 - len(text)) + text
    return cnpj_checks(text) == text[-2:]
