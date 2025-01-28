# Initialize HTML generator
html_generator = HTMLGenerator()

# Prepare LLLT protocol data for dashboard
lllt_dashboard_data = {
    "LLLT Daily Schedule": lllt_dfs["daily"],
    "LLLT Supplement Schedule": lllt_dfs["supplements"],
    "LLLT Weekly Schedule": lllt_dfs["weekly"],
    "LLLT Adjustments": adjustments_df
}

# Generate LLLT dashboard
lllt_html = html_generator.generate_dashboard(lllt_dashboard_data)
with open("data/raw/lllt_dashboard.html", "w") as f:
    f.write(lllt_html)

# Prepare Mobility protocol data for dashboard
mobility_dashboard_data = {
    "Phase 1 Morning": mobility_dfs["phase_phase1"]["morning"],
    "Phase 1 Lunch": mobility_dfs["phase_phase1"]["lunch"],
    "Phase 1 Pre-Bed": mobility_dfs["phase_phase1"]["pre_bed"],
    "Phase 2 Morning": mobility_dfs["phase_phase2"]["morning"],
    "Phase 2 Lunch": mobility_dfs["phase_phase2"]["lunch"],
    "Progress Metrics": progress_df,
    "Key Adjustments": adjustments_df
}

# Generate Mobility dashboard
mobility_html = html_generator.generate_dashboard(mobility_dashboard_data)
with open("data/raw/mobility_dashboard.html", "w") as f:
    f.write(mobility_html)

print("HTML dashboards generated successfully!") 