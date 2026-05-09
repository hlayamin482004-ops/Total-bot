import re

# Define cashback keywords and their percentages
cashback_keywords = {
    "du": {"percent": 0.07, "variations": ["du", "ဒူ", "ဒူဘိုင်း", "dubai"]},
    "me": {"percent": 0.07, "variations": ["me", "မီ", "မီဂါ", "mega"]},
    "maxi": {"percent": 0.07, "variations": ["maxi", "မက်ဆီ", "မက်စီ", "စီစီ", "max"]},
    "lao": {"percent": 0.07, "variations": ["lao", "လာလာ", "လာအို", "loa", "loadon", "laodon"]},
    "landon": {"percent": 0.07, "variations": ["landon", "လန်လန်", "လန်ဒန်", "ld", "london"]},
    "mm": {"percent": 0.10, "variations": ["mm", "မမ"]},
    "glo": {"percent": 0.03, "variations": ["glo", "ဂလို", "global"]},
}

# Compile regex for cashback keywords for efficient searching
cashback_regex_patterns = {}
for key, data in cashback_keywords.items():
    pattern = r"\b(?:" + "|".join(re.escape(v) for v in data["variations"]) + r")\b"
    cashback_regex_patterns[key] = re.compile(pattern, re.IGNORECASE)

# Define betting pattern keywords and their regex for extraction
# Prioritize more specific patterns by placing them earlier in the dictionary
betting_patterns = {
    "ကပ်": {"keywords": ["ကပ်", "အကပ်", "ကို"], "regex": r"(\d+)(?:ကို|k)(\d+)(?:ကပ်|kap)"},
    "ပတ်ပူး": {"keywords": ["ပတ်ပူး", "ပူးပို", "ပတ်ပူးပို", "ပတ်အကွက်20", "ထန", "ထပ", "ထိပ်ပိတ်", "ထိပ်နောက်"], "regex": r"(\d+)(?:ပတ်ပူး|ပူးပို|ပတ်ပူးပို|ပတ်အကွက်20|ထန|ထပ|ထိပ်ပိတ်|ထိပ်နောက်)"},
    "အပူးပါခွေ": {"keywords": ["အပူးပါခွေ", "ပူး", "အပူးပါ", "ခွေပူး", "အခွေပူး"], "regex": r"(\d+)(?:အပူးပါခွေ|ပူး|အပူးပါ|ခွေပူး|အခွေပူး)"},
    "ပတ်": {"keywords": ["ပတ်", "အပါ", "ပါ", "ch", "p"], "regex": r"(\d+)(?:ပတ်|အပါ|ပါ|ch|p)"},
    "ထိပ်": {"keywords": ["ထိပ်စီး", "ထိပ်", "ထ", "top", "t"], "regex": r"(\d+)(?:ထိပ်စီး|ထိပ်|ထ|top|t)"},
    "ဘရိတ်": {"keywords": ["ဘရိတ်", "bk"], "regex": r"(\d+)(?:ဘရိတ်|bk)"},
    "ခွေ": {"keywords": ["ခွေ", "အခွေ", "ခ"], "regex": r"(\d+)(?:ခွေ|အခွေ|ခ)"},
    "ဒဲ့": {"keywords": ["ဒဲ့"], "regex": r"(\d+)\s*(?:ဒဲ့)"},
    "R": {"keywords": ["r", "အာ"], "regex": r"(\d+)\s*(?:r|အာ)"},
    "ဆယ်ပြည့်": {"keywords": ["ဆယ်ပြည့်", "ဆယ်ပြည်", "ဆယ့်ပြည်"], "regex": r"(?:ဆယ်ပြည့်|ဆယ်ပြည်|ဆယ့်ပြည်)"},
    "စပူး": {"keywords": ["စပူး", "စုံပူး", "မပူး"], "regex": r"(?:စပူး|စုံပူး|မပူး)"},
    "အပူးစုံ": {"keywords": ["အပူးစုံ", "အပူး", "ပူး"], "regex": r"(?:အပူးစုံ|အပူး|ပူး)"},
    "စစ": {"keywords": ["စစ", "မမ", "စမ", "မစ", "စုံစုံ", "စုံမ", "စုူံစူံ", "စုံစုံ", "စုံစူံ"], "regex": r"(?:စစ|မမ|စမ|မစ|စုံစုံ|စုံမ|စုူံစူံ|စုံစုံ|စုံစူံ)"},
    "စုံဘရိတ်": {"keywords": ["စုံဘရိတ်", "စုံbk", "မbk", "စုံbk", "မဘရိတ်", "စဘရိတ်"], "regex": r"(?:စုံဘရိတ်|စုံbk|မbk|စုံbk|မဘရိတ်|စဘရိတ်)"},
    "ပါဝါ": {"keywords": ["ပါဝါ", "ပဝ", "pw", "power"], "regex": r"(?:ပါဝါ|ပဝ|pw|power)"},
    "နက္ခတ်": {"keywords": ["နက္ခတ်", "nk", "နက", "နခ"], "regex": r"(?:နက္ခတ်|nk|နက|နခ)"},
    "ညီကို": {"keywords": ["ညီကို", "ညီအကို", "ညီအစ်ကို"], "regex": r"(?:ညီကို|ညီအကို|ညီအစ်ကို)"},
}

# Compile regex for betting pattern keywords
betting_regex_patterns_compiled = {}
for key, data in betting_patterns.items():
    betting_regex_patterns_compiled[key] = re.compile(data["regex"], re.IGNORECASE)

def get_pair_numbers(digit: int, include_double: bool = False) -> list[int]:
    """Generates numbers containing the given digit for \'ပတ်\' and \'ပတ်ပူး\' patterns."""
    numbers = set()
    for i in range(100):
        s = str(i).zfill(2)
        if str(digit) in s:
            numbers.add(i)
    if include_double and (digit * 10 + digit) not in numbers:
        numbers.add(digit * 10 + digit) # Add the double if not already present
    return sorted(list(numbers))

def get_break_numbers(target_break: int) -> list[int]:
    """Generates numbers that sum up to the target break."""
    numbers = set()
    for i in range(100):
        if (i // 10 + i % 10) % 10 == target_break:
            numbers.add(i)
    return sorted(list(numbers))

def parse_betting_line(line: str):
    """Parses a single betting line and extracts numbers, keywords, and amounts."""
    original_line = line.strip()
    line = original_line.lower()

    parsed_data = {
        "original_line": original_line,
        "numbers": [], # Can be list of ints or list of lists of ints for \'ကပ်\'
        "bet_type_keywords": [],
        "amount_direct": 0,
        "amount_reverse": 0,
        "cashback_key": None,
        "cashback_percent": 0.0,
        "is_reverse_bet": False,
        "bet_pattern": None # To store the identified betting pattern
    }

    # 1. Extract Cashback Keyword and Percentage
    for cb_key, regex_pattern in cashback_regex_patterns.items():
        if regex_pattern.search(line):
            parsed_data["cashback_key"] = cb_key
            parsed_data["cashback_percent"] = cashback_keywords[cb_key]["percent"]
            for variation in cashback_keywords[cb_key]["variations"]:
                line = line.replace(variation.lower(), " ")
            break

    # 2. Extract Amount(s) - handle 500R250 pattern first
    amount_r_match = re.search(r'(\d+)[rR](\d+)$', line)
    if amount_r_match:
        parsed_data["amount_direct"] = int(amount_r_match.group(1))
        parsed_data["amount_reverse"] = int(amount_r_match.group(2))
        parsed_data["is_reverse_bet"] = True
        line = line[:amount_r_match.start()] # Remove amount part from line
    else:
        single_amount_match = re.search(r'(\d+)$', line)
        if single_amount_match:
            parsed_data["amount_direct"] = int(single_amount_match.group(1))
            line = line[:single_amount_match.start()] # Remove amount part from line

    line = re.sub(r'[\s\-\=\*\/]+', ' ', line).strip()

    # 3. Identify Betting Pattern and Extract Numbers/Keywords accordingly
    # Iterate through patterns in a defined order (most specific first)
    for pattern_key, data in betting_patterns.items():
        regex_pattern_compiled = betting_regex_patterns_compiled[pattern_key]
        match = regex_pattern_compiled.search(line)
        if match:
            parsed_data["bet_pattern"] = pattern_key
            if pattern_key == "ကပ်":
                first_set_str = match.group(1)
                second_set_str = match.group(2)
                parsed_data["numbers"] = [[int(d) for d in list(first_set_str)], [int(d) for d in list(second_set_str)]]
            elif len(match.groups()) > 0 and match.group(1).isdigit():
                # For patterns like \'123ခွေ\', \'9ပတ်\', etc.
                parsed_data["numbers"] = [int(d) for d in list(match.group(1))]
            
            # Remove the matched part from the line to avoid re-processing
            line = line.replace(match.group(0), " ")
            line = re.sub(r'\s+', ' ', line).strip()
            break # Found a pattern, move on

    # General number and keyword extraction for remaining parts
    parts = line.split()
    temp_numbers = []
    temp_keywords = []

    for part in parts:
        if re.fullmatch(r'\d+', part): # Check if the part is purely digits
            temp_numbers.append(int(part))
        else:
            temp_keywords.append(part)

    # If numbers were not extracted by a specific pattern regex, use temp_numbers
    if not parsed_data["numbers"] and temp_numbers:
        parsed_data["numbers"] = temp_numbers
    
    parsed_data["bet_type_keywords"] = temp_keywords

    # Check for \'R\' as a standalone keyword if not already handled in amount
    if 'r' in parsed_data["bet_type_keywords"] and not parsed_data["is_reverse_bet"]:
        parsed_data["is_reverse_bet"] = True
        parsed_data["bet_type_keywords"].remove('r')

    return parsed_data

def calculate_total_amount(parsed_data: dict):
    """Calculates the total amount for a parsed betting line based on betting patterns."""
    total_blocks = 0
    amount_per_block_direct = parsed_data["amount_direct"]
    amount_per_block_reverse = parsed_data["amount_reverse"]

    bet_pattern = parsed_data["bet_pattern"]
    numbers = parsed_data["numbers"]
    is_reverse_bet = parsed_data["is_reverse_bet"]

    if bet_pattern == "ဒဲ့" or (not bet_pattern and numbers and not (isinstance(numbers, list) and len(numbers) > 0 and isinstance(numbers[0], list))): # Default to ဒဲ့ if no specific pattern but numbers are present and not \'ကပ်\'
        total_blocks = len(numbers)
        if is_reverse_bet:
            total_blocks *= 2
    elif bet_pattern == "ပတ်":
        if numbers and not (isinstance(numbers, list) and len(numbers) > 0 and isinstance(numbers[0], list)):
            for digit in numbers:
                total_blocks += len(get_pair_numbers(digit, include_double=False)) # 19 blocks
        else:
            total_blocks = 10 * 19 # 10 digits * 19 blocks each
    elif bet_pattern == "ပတ်ပူး":
        if numbers and not (isinstance(numbers, list) and len(numbers) > 0 and isinstance(numbers[0], list)):
            for digit in numbers:
                total_blocks += len(get_pair_numbers(digit, include_double=True)) # 20 blocks
        else:
            total_blocks = 10 * 20 # 10 digits * 20 blocks each
    elif bet_pattern == "ထိပ်":
        if numbers and not (isinstance(numbers, list) and len(numbers) > 0 and isinstance(numbers[0], list)):
            total_blocks = len(numbers) * 10 # Each number represents 10 \'top\' numbers
        else:
            total_blocks = 10 * 10
    elif bet_pattern == "ဘရိတ်":
        if numbers and not (isinstance(numbers, list) and len(numbers) > 0 and isinstance(numbers[0], list)):
            for target_break in numbers:
                total_blocks += len(get_break_numbers(target_break)) # 10 blocks for each break
        else:
            total_blocks = 10 * 10
    elif bet_pattern == "ခွေ":
        if len(numbers) >= 2 and not (isinstance(numbers, list) and len(numbers) > 0 and isinstance(numbers[0], list)):
            n = len(numbers)
            total_blocks = n * (n - 1) # n * (n-1) combinations without doubles
        # else: need more context for single digit \'ခွေ\'
    elif bet_pattern == "အပူးပါခွေ":
        if len(numbers) >= 1 and not (isinstance(numbers, list) and len(numbers) > 0 and isinstance(numbers[0], list)):
            n = len(numbers)
            total_blocks = n * n # n * n combinations with doubles
        # else: need more context for no digit \'အပူးပါခွေ\'
    elif bet_pattern == "ဆယ်ပြည့်":
        total_blocks = 10 # 10, 20, ..., 00
    elif bet_pattern == "အပူးစုံ":
        total_blocks = 10 # 00, 11, ..., 99
    elif bet_pattern == "စပူး":
        total_blocks = 5 # Even doubles or Odd doubles
    elif bet_pattern == "စစ":
        total_blocks = 25
        if is_reverse_bet:
            total_blocks *= 2
    elif bet_pattern == "ကပ်":
        if len(numbers) == 2 and isinstance(numbers[0], list) and isinstance(numbers[1], list):
            a = len(numbers[0])
            b = len(numbers[1])
            total_blocks = a * b
            if is_reverse_bet:
                total_blocks *= 2
    elif bet_pattern == "စုံဘရိတ်":
        total_blocks = 50
    elif bet_pattern == "ပါဝါ":
        total_blocks = 10
    elif bet_pattern == "နက္ခတ်":
        total_blocks = 10
    elif bet_pattern == "ညီကို":
        total_blocks = 20

    total_bet_amount = (total_blocks * amount_per_block_direct) + \
                       (total_blocks * amount_per_block_reverse if is_reverse_bet else 0)

    return total_bet_amount

def format_output(user_name: str, total_bet_amount: float, cashback_percent: float, cashback_key: str):
    """Formats the output string as per user\'s example."""
    cashback_amount = total_bet_amount * cashback_percent
    net_amount = total_bet_amount - cashback_amount

    cashback_line = ""
    if cashback_key:
        # Capitalize the first letter of the cashback key for display
        display_cashback_key = cashback_key.capitalize()
        cashback_line = f" {display_cashback_key} {int(cashback_percent * 100)}% Cashback = {cashback_amount:,.0f} ကျပ်\\n--------------------\\n"

    output_str = f"👤 {user_name}\\n--------------------\\n စုစုပေါင်း = {total_bet_amount:,.0f} ကျပ်\\n{cashback_line}လက်ခံရမည့်ငွေ = {net_amount:,.0f} ကျပ် ဘဲ လွဲပါရှင့်\\n--------------------\\nကံကောင်းပါစေ"
    return output_str

# Placeholder for testing
if __name__ == "__main__":
    test_lines = [
        "らŤΛ尺: 2468ခွေပုး1600", # Example from user - this will need more specific parsing for \'ခွေပူး\'
        "456ပတ်700", # Example from user
        "790bk700", # Example from user - this will need more specific parsing for \'bk\'
        "Du 12 500", # Test with cashback keyword
        "12 500",
        "12-500",
        "12=500",
        "12 ဒဲ့ 500",
        "12r 500",
        "23 45 56=500R250", # Complex R pattern
        "Me 123 1000", # Another cashback test
        "Mm 456 2000",
        "12r 500",
        "9ပတ် 1000", # Test \'ပတ်\'
        "9ပတ်အပူးပို 1000", # Test \'ပတ်ပူး\'
        "ပတ် 1000", # Test \'ပတ်\' without specific number
        "ပတ်ပူး 1000", # Test \'ပတ်ပူး\' without specific number
        "2ထိပ် 500", # Test \'ထိပ်\'
        "ထိပ် 500", # Test \'ထိပ်\' without specific number
        "1ဘရိတ် 1000", # Test \'ဘရိတ်\'
        "ဘရိတ် 1000", # Test \'ဘရိတ်\' without specific number
        "123ခွေ 500", # Test \'ခွေ\'
        "123ပူး 500", # Test \'အပူးပါခွေ\'
        "ဆယ်ပြည့် 1000", # Test \'ဆယ်ပြည့်\'
        "အပူး 500", # Test \'အပူးစုံ\'
        "စပူး 500", # Test \'စပူး\'
        "စမ 500", # Test \'စစ\'
        "စုံဘရိတ် 500", # Test \'စုံဘရိတ်\'
        "ပါဝါ 1000", # Test \'ပါဝါ\'
        "နက္ခတ် 1000", # Test \'နက္ခတ်\'
        "ညီကို 1000", # Test \'ညီကို\'
        "234ကို678ကပ်R 1000" # Test \'ကပ်\' with R
    ]

    print("--- Parsing Test ---")
    for line in test_lines:
        parsed = parse_betting_line(line)
        print(f"Original: {line}")
        print(f"Parsed: {parsed}")
        total_bet = calculate_total_amount(parsed)
        print(f"Calculated Total (basic): {total_bet}")
        user_name = "TestUser"
        formatted_output = format_output(user_name, total_bet, parsed["cashback_percent"], parsed["cashback_key"])
        print(f"Formatted Output:\n{formatted_output}")
        print("\n" + "="*30 + "\n")
