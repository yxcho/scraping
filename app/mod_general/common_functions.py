import pandas as pd

# function to make all values numerical


def convert_to_numeric(column):
    first_col = [i.replace(',', '') for i in column]
    second_col = [i.replace('-', '') for i in first_col]
    final_col = pd.to_numeric(second_col)

    return final_col


def convert_to_digits(numString: str) -> int:
    """
    Convert "570.68B" to 570680000000, "32.7m" to 32760000
    """
    try:
        numOfZeroes = {"T": 12, "B": 9, "M": 6, "K": 3}
        numInt = numString
        unit = numString[-1].upper()
        if unit in numOfZeroes:
            numString = numString[:-1]
            numFloat = float(numString)
            numInt = int(numFloat * pow(10, numOfZeroes[unit]))
        return numInt
    except Exception as e:
        print(f"Exception raised: {e}")


def convert_percentage_to_float(percent_str: str) -> float:
    """
    Convert "27.56%" to 0.2756
    """
    try:
        if percent_str[-1] == "%":
            return float(percent_str[:-1])/100
    except Exception as e:
        print(f"Exception raised: {e}")
