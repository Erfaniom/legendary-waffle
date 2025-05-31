import streamlit as st

st.set_page_config(page_title="Economic Project Comparator")

st.title("📊 Economic Project Comparator")

inflation = st.number_input("Global Inflation Rate (%)", value=5.0) / 100

project_count = st.number_input("How many projects?", min_value=1, step=1)

projects = []

for i in range(int(project_count)):
    st.subheader(f"Project {i + 1}")
    name = st.text_input(f"Project {i + 1} Name", value=f"Project {i + 1}")
    investment = st.number_input(f"{name} - Initial Investment", key=f"inv_{i}")
    salvage = st.number_input(f"{name} - Salvage Value", key=f"salvage_{i}")
    years = st.number_input(f"{name} - Project Duration (years)", min_value=1, step=1, key=f"years_{i}")
    operation = st.number_input(f"{name} - Annual Operation Cost", key=f"op_{i}")
    income = st.number_input(f"{name} - Annual Income", key=f"inc_{i}")
    
    projects.append({
        "name": name,
        "investment": investment,
        "salvage": salvage,
        "years": years,
        "operation": operation,
        "income": income,
    })

def calculate_npw(p, inflation):
    npw = -p["investment"]
    for t in range(1, int(p["years"]) + 1):
        discount = (1 + inflation) ** -t
        npw += (p["income"] - p["operation"]) * discount
    npw += p["salvage"] * ((1 + inflation) ** -p["years"])
    return npw

def calculate_bcr(p, inflation):
    benefits = 0
    costs = p["investment"]
    for t in range(1, int(p["years"]) + 1):
        discount = (1 + inflation) ** -t
        benefits += p["income"] * discount
        costs += p["operation"] * discount
    benefits += p["salvage"] * ((1 + inflation) ** -p["years"])
    return benefits / costs if costs != 0 else float('inf')

if st.button("🔍 Evaluate Projects"):
    results = []
    for p in projects:
        npw = calculate_npw(p, inflation)
        bcr = calculate_bcr(p, inflation)
        results.append({**p, "npw": npw, "bcr": bcr})

    if results:
        best = max(results, key=lambda x: x["npw"])
        st.success(f"🏆 Most Economically Viable: {best['name']} (NPW: ${best['npw']:.2f}, BCR: {best['bcr']:.2f})")
        st.write("---")
        for r in results:
            st.markdown(f"### {r['name']}")
            st.write(f"**NPW:** ${r['npw']:.2f}")
            st.write(f"**Benefit-Cost Ratio:** {r['bcr']:.2f}")
