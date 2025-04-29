
import re

def extract_financials(text):
    patterns = {
        "Revenue": r"(?:total )?revenue[^\d]*(\d+[.,]?\d*)",
        "Costs": r"(?:total )?(?:costs|expenses)[^\d]*(\d+[.,]?\d*)",
        "EBITDA": r"EBITDA[^\d]*(\d+[.,]?\d*)",
        "Net Profit": r"net (?:income|profit)[^\d]*(\d+[.,]?\d*)"
    }
    data = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                data[key] = float(match.group(1).replace(',', ''))
            except ValueError:
                pass
    return data if data else None
