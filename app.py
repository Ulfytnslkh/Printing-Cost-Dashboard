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
        .str.strip()      # hapus spasi depan/belakang
        .str.upper()      # kapital
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
        df.groupby(col_month)[
            [
                "BW_PAGES",
                "COLOR_PAGES",
                "TOTAL_PAGES",
                "BW_COST",
                "COLOR_COST",
                "TOTAL_COST",
            ]
        ]
        .sum()
        .reset_index()
        .rename(columns={col_month: "PERIOD"})
    )

    monthly = monthly[monthly["PERIOD"].isin(MONTH_ORDER)]

    monthly["PERIOD"] = pd.Categorical(
        monthly["PERIOD"],
        categories=MONTH_ORDER,
        ordered=True
    )
    monthly = monthly.sort_values("PERIOD")

    dept = (
        df.groupby(col_dept)[
            ["BW_PAGES", "COLOR_PAGES", "TOTAL_PAGES", "TOTAL_COST"]
        ]
        .sum()
        .reset_index()
        .rename(columns={col_dept: "DEPARTMENT"})
    )

    dept = dept[dept["DEPARTMENT"].notna() & (dept["DEPARTMENT"] != "")]

    return df, monthly, dept
