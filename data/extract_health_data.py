import pandas as pd

# LLLT Protocol - Supplement Schedule (exactly as in notebook)
data_lllt_supplements = [
    {
        "Time": "Post-AM LLLT",
        "Supplements": "Collagen + vitamin C + silicium",
        "Purpose": "Skin/hair collagen synthesis."
    },
    {
        "Time": "Post-PM LLLT",
        "Supplements": "Omega-3s + magnesium",
        "Purpose": "Muscle recovery + anti-inflammatory."
    },
    {
        "Time": "Pre-Bed",
        "Supplements": "L-theanine + tryptophan",
        "Purpose": "Stress reduction + sleep."
    }
]

# LLLT Protocol - Daily Schedule (exactly as in notebook)
data_lllt_daily = [
    {
        "Day Type": "LLLT Days",
        "Frequency": "3 days/week",
        "Example Days": "Mon/Wed/Fri",
        "Focus": "Hair + Body Optimization",
        "Key Principle": "Synced supplements amplify collagen/antioxidants"
    },
    {
        "Day Type": "Rest Days",
        "Frequency": "3 days/week",
        "Example Days": "Tue/Thu/Sat/Sun",
        "Focus": "Mitochondrial recovery",
        "Key Principle": "Hydration, diet, stress management"
    },
    {
        "Day Type": "Flexible Day",
        "Frequency": "1 day/week",
        "Example Days": "Sun",
        "Focus": "System reset (no LLLT/Dutasteride)",
        "Key Principle": "Optional light cardio or rest"
    }
]

# Create DataFrames exactly as they appear in the notebook
lllt_supplements_df = pd.DataFrame(data_lllt_supplements)
lllt_daily_df = pd.DataFrame(data_lllt_daily)

# Save DataFrames to CSV
lllt_supplements_df.to_csv('data/lllt_supplements.csv', index=False)
lllt_daily_df.to_csv('data/lllt_daily.csv', index=False)

print("LLLT data has been extracted from the notebook and saved to CSV files.")
print("Note: Mobility data extraction is pending until we can access the complete notebook content.") 