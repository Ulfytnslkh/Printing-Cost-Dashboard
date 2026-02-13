import pandas as pd

MONTH_ORDER = [
    "JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE",
    "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"
]

def prepare_summary(
    df,
    col_month,
    col_dept,
    col_bw,
    col_color,
    bw_price,
    color_price
):
    df = df.copy()

    
    df[col_month] = (
        df[col_month]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    df = df[df[col_month].isin(MONTH_ORDER)]

    # Jadikan kategori berurutan
    df[col_month] = pd.Categorical(
        df[col_month],
        categories=MONTH_ORDER,
        ordered=True
    )

    
    df[col_bw] = pd.to_numeric(df[col_bw], errors="coerce").fillna(0)
    df[col_color] = pd.to_numeric(df[col_color], errors="coerce").fillna(0)

   
    df["BW_PAGES"] = df[col_bw]
    df["COLOR_PAGES"] = df[col_color]
    df["TOTAL_PAGES"] = df["BW_PAGES"] + df["COLOR_PAGES"]

    
    df["BW_COST"] = df["BW_PAGES"] * bw_price
    df["COLOR_COST"] = df["COLOR_PAGES"] * color_price
    df["TOTAL_COST"] = df["BW_COST"] + df["COLOR_COST"]

   
    monthly = (
        df.groupby(col_month, observed=True)[
            ["BW_PAGES", "COLOR_PAGES", "TOTAL_PAGES",
             "BW_COST", "COLOR_COST", "TOTAL_COST"]
        ]
        .sum()
        .reset_index()
        .rename(columns={col_month: "PERIOD"})
        .sort_values("PERIOD")
    )

    
    monthly = monthly[
        (monthly["TOTAL_PAGES"] > 0) &
        (monthly["TOTAL_COST"] > 0)
    ]

   
    dept = (
        df.groupby(col_dept)[
            ["BW_PAGES", "COLOR_PAGES", "TOTAL_PAGES", "TOTAL_COST"]
        ]
        .sum()
        .reset_index()
        .rename(columns={col_dept: "DEPARTMENT"})
    )

   
    dept = dept[
        (dept["TOTAL_PAGES"] > 0) &
        (dept["TOTAL_COST"] > 0)
    ]

    return df, monthly, dept
