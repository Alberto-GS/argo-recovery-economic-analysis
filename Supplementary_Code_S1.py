"""
Supplementary Material S1
code/Supplementary_Code_ArgoRecovery.py

Code used to reproduce:
- Table 2 (Deterministic baseline model)
- Figure 1 (Sensitivity analysis)
- Figure 2 (Mission-level ECUF analysis)
- Table 3 (Monte Carlo simulation)
- Figure 3 (Monte Carlo results)
- Table 5 (Cost-per-profile analysis)

Tested with:
Python 3.12
NumPy 2.x
Pandas 2.x
Matplotlib 3.x

Author:
Luis Miret et al.
"""

# ==========================================================
# IMPORTS
# ==========================================================
import platform
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

print("Python version:", platform.python_version())
print("NumPy version:", np.__version__)
print("Pandas version:", pd.__version__)
print("Matplotlib version:", plt.matplotlib.__version__)

np.random.seed(42)

# ==========================================================
# 1. INPUT PARAMETERS
# ==========================================================
MISSION_COST = 85000
MISSION_SIGMA = 0.25
N_FLOATS = 10
FAILURE_PROBABILITY = 0.12
SUCCESS_PROBABILITY = 1 - FAILURE_PROBABILITY
N_ITER = 50000

FLOATS = {
    "Core": {
        "new_cost": 24000,
        "repair_transport": 9000
    },
    "Deep": {
        "new_cost": 60000,
        "repair_transport": 10000
    },
    "BGC (O2)": {
        "new_cost": 50000,
        "repair_transport": 22000
    },
    "BGC (O2, FLBB)": {
        "new_cost": 70000,
        "repair_transport": 22000
    },
    "BGC (+3)": {
        "new_cost": 150000,
        "repair_transport": 22000
    }
}

# ==========================================================
# 2. DETERMINISTIC BASELINE CALCULATIONS (TABLE 2)
# ==========================================================
#
# IRT = Cnew − (Crepair + Ctransport)
#
# ==========================================================
table2 = []
for float_type, pars in FLOATS.items():
    irt = pars["new_cost"] - pars["repair_transport"]
    table2.append([
        float_type,
        pars["new_cost"],
        pars["repair_transport"],
        irt
    ])

table2 = pd.DataFrame(
    table2,
    columns=[
        "Float type",
        "Acquisition cost (€)",
        "Repair + transport (€)",
        "IRT (€)"
    ]
)

print("\nTABLE 2")
print(table2)

table2.to_excel("Table2_IRT.xlsx", index=False)
table2.to_csv("Table2_IRT.csv", index=False)

# ==========================================================
# 3. SENSITIVITY ANALYSIS (FIGURE 1)
# Updated using observed redeployment lifetimes
# ==========================================================
core = {
    "Recovery cost": (-4700, 4700),
    "Post-repair lifetime": (
        15000 * ((0.81 / 0.91) - 1), 
        15000 * ((1.01 / 0.91) - 1)
    ),
    "Non-reusable floats": (-2000, 2000)
}

deep = {
    "Recovery cost": (-5000, 5000),
    "Post-repair lifetime": (
        50000 * ((0.43 / 0.48) - 1), 
        50000 * ((0.53 / 0.48) - 1)
    ),
    "Non-reusable floats": (-2600, 2600)
}

bgc = {
    "Recovery cost": (-5500, 5500),
    "Post-repair lifetime": (
        128000 * ((0.42 / 0.51) - 1), 
        128000 * ((0.60 / 0.51) - 1)
    ),
    "Non-reusable floats": (-3000, 3000)
}

fig, axes = plt.subplots(1, 3, figsize=(14, 5))

datasets = [
    ("Core (IRT = €15k)", core),
    ("Deep (IRT = €50k)", deep),
    ("BGC (+3) (IRT = €128k)", bgc)
]

for ax, (title, data) in zip(axes, datasets):
    # Order variables by maximum absolute impact
    variables = sorted(
        data.keys(),
        key=lambda x: max(abs(data[x][0]), abs(data[x][1])),
        reverse=True
    )
    low = [data[v][0] for v in variables]
    high = [data[v][1] for v in variables]
    y = np.arange(len(variables))

    ax.barh(y, low, color="steelblue", label="Lower bound")
    ax.barh(y, high, color="darkorange", label="Upper bound")
    ax.axvline(0, color="black", linewidth=1)
    ax.set_yticks(y)
    ax.set_yticklabels(variables)
    ax.set_title(title)
    ax.invert_yaxis()
    ax.set_xlabel("Change in Economic Margin (€)")

axes[0].legend()
plt.tight_layout()
plt.savefig("Figure1_Sensitivity_Updated.png", dpi=300, bbox_inches="tight")

# ==========================================================
# 4. MISSION-LEVEL ECUF ANALYSIS (FIGURE 2)
# ==========================================================
q_values = np.arange(0, 0.52, 0.02)

colors = {
    "Core": "black",
    "Deep": "0.25",
    "BGC (O2)": "0.45",
    "BGC (O2, FLBB)": "0.65",
    "BGC (+3)": "0.85"
}

fig, axes = plt.subplots(1, 2, figsize=(13, 6))

# PANEL A
for float_type in ["Core", "Deep", "BGC (O2)"]:
    pars = FLOATS[float_type]
    ecuf = (MISSION_COST / (N_FLOATS * (1 - q_values))) + pars["repair_transport"]
    axes[0].plot(q_values, ecuf, color=colors[float_type], linewidth=2, label=float_type)
    axes[0].axhline(pars["new_cost"], linestyle="--", linewidth=1, alpha=0.6, color=colors[float_type])

axes[0].set_xlabel("Proportion of non-reusable floats")
axes[0].set_ylabel("ECUF (€)")
axes[0].text(-0.10, 1.03, "A", transform=axes[0].transAxes, fontsize=16, fontweight="bold")

# PANEL B
for float_type in ["BGC (O2, FLBB)", "BGC (+3)"]:
    pars = FLOATS[float_type]
    ecuf = (MISSION_COST / (N_FLOATS * (1 - q_values))) + pars["repair_transport"]
    axes[1].plot(q_values, ecuf, color=colors[float_type], linewidth=2, label=float_type)
    axes[1].axhline(pars["new_cost"], linestyle="--", linewidth=1, alpha=0.6, color=colors[float_type])

axes[1].set_xlabel("Proportion of non-reusable floats")
axes[1].text(-0.10, 1.03, "B", transform=axes[1].transAxes, fontsize=16, fontweight="bold")

# SINGLE LEGEND
handles, labels = [], []
for ax in axes:
    h, l = ax.get_legend_handles_labels()
    handles.extend(h)
    labels.extend(l)

fig.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.5, -0.05), ncol=5, frameon=False)
fig.subplots_adjust(bottom=0.22, wspace=0.25)
plt.savefig("Figure2_ECUF.png", dpi=600, bbox_inches="tight")

# ==========================================================
# 5. MONTE CARLO SIMULATION
# ==========================================================
mu = np.log(MISSION_COST) - (MISSION_SIGMA**2) / 2

mission_cost = np.random.lognormal(mean=mu, sigma=MISSION_SIGMA, size=N_ITER)
n_useful = np.random.binomial(n=N_FLOATS, p=SUCCESS_PROBABILITY, size=N_ITER)

results = []
ecuf_summary = {}

for float_type, pars in FLOATS.items():
    ecuf = np.full(N_ITER, np.inf)
    valid = n_useful > 0
    ecuf[valid] = (mission_cost[valid] / n_useful[valid]) + pars["repair_transport"]
    
    viable = ecuf < pars["new_cost"]
    finite_ecuf = ecuf[np.isfinite(ecuf)]
    ecuf_summary[float_type] = finite_ecuf

    results.append({
        "Float type": float_type,
        "Probability of viability (%)": 100 * viable.mean(),
        "Median ECUF (€)": np.median(finite_ecuf),
        "P10 (€)": np.percentile(finite_ecuf, 10),
        "P90 (€)": np.percentile(finite_ecuf, 90)
    })

table3 = pd.DataFrame(results)

print("\nTABLE 3")
print(table3.round(2))

table3.to_excel("Table3_MonteCarlo.xlsx", index=False)
table3.to_csv("Table3_MonteCarlo.csv", index=False)

# FIGURE 3
fig, axes = plt.subplots(1, 2, figsize=(13, 6), sharey=False)

# PANEL A
panelA = ["Core", "Deep", "BGC (O2)"]
labels, medians, p10, p90 = [], [], [], []

for f in panelA:
    values = ecuf_summary[f]
    labels.append(f)
    medians.append(np.median(values))
    p10.append(np.percentile(values, 10))
    p90.append(np.percentile(values, 90))

yerr = [
    np.array(medians) - np.array(p10),
    np.array(p90) - np.array(medians)
]

axes[0].errorbar(labels, medians, yerr=yerr, fmt="o", color="black")

for f in panelA:
    axes[0].axhline(FLOATS[f]["new_cost"], linestyle="--", alpha=0.4)

axes[0].set_ylabel("ECUF (€)")
axes[0].set_title("Core, Deep and BGC (O₂)")
axes[0].text(-0.12, 1.03, "A", transform=axes[0].transAxes, fontsize=16, fontweight="bold")

# PANEL B
panelB = ["BGC (O2, FLBB)", "BGC (+3)"]
labels, medians, p10, p90 = [], [], [], []

for f in panelB:
    values = ecuf_summary[f]
    labels.append(f)
    medians.append(np.median(values))
    p10.append(np.percentile(values, 10))
    p90.append(np.percentile(values, 90))

yerr = [
    np.array(medians) - np.array(p10),
    np.array(p90) - np.array(medians)
]

axes[1].errorbar(labels, medians, yerr=yerr, fmt="o", color="black")

for f in panelB:
    axes[1].axhline(FLOATS[f]["new_cost"], linestyle="--", alpha=0.4)

axes[1].set_title("Advanced BGC configurations")
axes[1].text(-0.12, 1.03, "B", transform=axes[1].transAxes, fontsize=16, fontweight="bold")

axes[0].set_ylim(0, 70000)
axes[1].set_ylim(0, 160000)

plt.tight_layout()
plt.savefig("Figure3_MonteCarlo.png", dpi=600, bbox_inches="tight")

# ==========================================================
# 6. COST-PER-PROFILE CALCULATIONS (TABLE 5)
# ==========================================================
# Número medio de perfiles por tipo de flotador (Tabla 1)
PROFILE_DATA = {
    "Core": 169,
    "Deep": 77,
    "BGC (+3)": 99
}

table5_data = []

for float_type, n_profiles in PROFILE_DATA.items():
    acquisition_cost = FLOATS[float_type]["new_cost"]
    cpp = acquisition_cost / n_profiles
    
    table5_data.append({
        "Float type": float_type,
        "Acquisition cost (€)": acquisition_cost,
        "Average profiles": n_profiles,
        "Cost per profile (€)": round(cpp, 2)
    })

table5 = pd.DataFrame(table5_data)

print("\nTABLE 5")
print(table5)

# Guardar los resultados en archivos
table5.to_excel("Table4_CostPerProfile.xlsx", index=False)
table5.to_csv("Table4_CostPerProfile.csv", index=False)
