def recommend_funds(profile):
 
    funds = {
        "High Risk": [
            "Axis Small Cap Fund",
            "SBI Small Cap Fund",
            "Nippon India Growth Fund"
        ],
 
        "Moderate Risk": [
            "Mirae Asset Large & Midcap Fund",
            "ICICI Prudential Bluechip Fund"
        ],
 
        "Low Risk": [
            "HDFC Balanced Advantage Fund",
            "ICICI Prudential Equity Savings Fund"
        ]
    }
 
    funds_list = funds.get(profile, [])
 
    # Fix: warn if profile key is unrecognised so silent empty-list bugs are visible
    if not funds_list:
        print(f"WARNING: No funds found for profile '{profile}'. "
              f"Expected one of: {list(funds.keys())}")
 
    return funds_list