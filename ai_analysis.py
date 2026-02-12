def generate_insight(monthly, dept):
    insights = []

    # Bulan paling mahal
    max_cost_row = monthly.loc[monthly["TOTAL_COST"].idxmax()]
    insights.append(
        f"Bulan dengan biaya tertinggi adalah **{max_cost_row['PERIOD']}** "
        f"dengan total Rp{int(max_cost_row['TOTAL_COST']):,}."
    )

    # Dominasi BW vs Color
    bw_total = monthly["BW_PAGES"].sum()
    color_total = monthly["COLOR_PAGES"].sum()

    if bw_total > color_total:
        insights.append(
            "Penggunaan kertas **hitam putih lebih dominan** dibandingkan warna."
        )
    else:
        insights.append(
            "Penggunaan kertas **warna cukup signifikan**, perlu evaluasi kebijakan."
        )

    # Departemen tertinggi
    top_dept = dept.sort_values("TOTAL_COST", ascending=False).iloc[0]
    insights.append(
        f"Departemen dengan biaya tertinggi adalah "
        f"**{top_dept['DEPARTMENT']}** "
        f"(Rp{int(top_dept['TOTAL_COST']):,})."
    )

    # Rekomendasi
    insights.append(
        "Rekomendasi: lakukan kontrol printing pada departemen dengan volume "
        "dan biaya tertinggi serta evaluasi penggunaan warna."
    )

    return insights
