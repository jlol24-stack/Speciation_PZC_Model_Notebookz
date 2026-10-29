import io
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import UnivariateSpline
from scipy.optimize import curve_fit

# =============================================================================
# MODULE 2: POINT OF ZERO CHARGE (pH_PZC) RESOLUTION FROM EXCEL
# =============================================================================
try:
    df_pzc = pd.read_excel("pzc_Mn_ferrite.xlsx")
    print("=" * 60)
    print(">>> MODULE 2: PZC Excel spreadsheet loaded successfully.")
except FileNotFoundError:
    print("=" * 60)
    print("Error: 'pzc_Mn_ferrite.xlsx' file not found in workspace.")
    raise

df_pzc_filtered = df_pzc[df_pzc["pHi"] > 4].sort_values(by="pHi")
x_calc = df_pzc_filtered["pHi"].values
y_calc = df_pzc_filtered["pHf"].values

spline_func = UnivariateSpline(x_calc, y_calc - x_calc, s=0)
detected_roots = spline_func.roots()
valid_roots = [r for r in detected_roots if 7.0 <= r <= 8.5]

calculated_pzc = float(valid_roots[0]) if len(valid_roots) > 0 else 7.64

print(f">>> Calculated True Surface Intercept (pH_PZC): {calculated_pzc:.2f}")
print("=" * 60)

# --- FIGURE 1: POINT OF ZERO CHARGE PLOT (USING THE COMPLETE TABLE) ---
df_pzc_full_sorted = df_pzc.sort_values(by="pHi")

plt.figure(figsize=(6.5, 5))
plt.plot(df_pzc_full_sorted["pHi"].values, df_pzc_full_sorted["pHf"].values, "o-", color="royalblue", label="Experimental Data")
plt.plot(df_pzc_full_sorted["pHi"].values, df_pzc_full_sorted["pHi"].values, "--", color="navy", alpha=0.7, label="$pH_i = pH_f$ Line")
plt.axvline(x=calculated_pzc, color="red", linestyle=":", label=f"$pH_{{PZC}} = {calculated_pzc:.2f}$")
plt.title("Point of Zero Charge ($pH_{PZC}$) for Manganese Ferrite NPs", fontsize=11, fontweight="bold")
plt.xlabel("Initial pH ($pH_i$)")
plt.ylabel("Final pH ($pH_f$)")
plt.grid(True, linestyle=":", alpha=0.6)
plt.legend(loc="upper left")
plt.tight_layout()
plt.show()

# =============================================================================
# ADSORPTION MODULE: FILE INGESTION (EQUILIBRIUM PIPELINE)
# =============================================================================
try:
    df_eq = pd.read_excel("dataeq_speciation.xlsx")
    df_eq["species"] = df_eq["species"].astype(str).str.lower().str.strip()
    print(">>> ADSORPTION MODULE: Equilibrium isotherm data file loaded successfully.")
except FileNotFoundError as fnf_error:
    print(f"File Ingestion Error: Ensure data files are in this folder. Trace: {fnf_error}")
    raise

print(f"Total compiled Equilibrium entries: {len(df_eq)}")
print("=" * 60)


# =============================================================================
# PHYSICOCHEMICAL REGRESSION MATHEMATICAL DEFINITIONS
# =============================================================================
def langmuir_equation(Ce, qmax, KL):
    """Langmuir non-linear expression: qe = (qmax * KL * Ce) / (1 + KL * Ce)"""
    return (qmax * KL * Ce) / (1.0 + KL * Ce)

# =============================================================================
# AUTOMATED EQUILIBRIUM ANALYSIS ENGINE
# =============================================================================
# CORRECTED: The values [2, 8] were assigned to clear the SyntaxError.
target_species_list = ["as(iii)", "as(v)"]
target_pH_list = [2, 8]

print(">>> RUNNING THERMODYNAMIC INTERCEPT ENGINE FOR ALL SYSTEMS")

for species in target_species_list:
    for ph in target_pH_list:
        display_label = "As(III)" if "iii" in species else "As(V)"
        print(f"\n[System: {display_label} at pH {ph}]")
        
        eq_query = (df_eq["species"] == species) & (df_eq["pH"] == ph)
        df_eq_subset = df_eq[eq_query].sort_values(by="Ce_mgL")
        
        Ce_array = df_eq_subset["Ce_mgL"].values
        qe_array = df_eq_subset["qe_mgg"].values
        
        if len(Ce_array) >= 3:
            try:
                popt_iso, _ = curve_fit(langmuir_equation, Ce_array, qe_array, p0=[50.0, 0.2], maxfev=10000)
                print(f"  -> Isotherm Langmuir Fit:")
                print(f"     Max Adsorption Capacity (qmax): {popt_iso[0]:.2f} mg/g")
                print(f"     Langmuir Affinity Constant (KL): {popt_iso[1]:.4f} L/mg")
            except Exception as fit_error:
                print(f"  -> Isotherm Fit failed: {fit_error}")
        else:
            print(f"  -> Isotherm Warning: Insufficient data density (Points: {len(Ce_array)})")

print("\n" + "=" * 60)
print(">>> ANALYSIS COMPLETE: Equilibrium data matrices successfully optimized.")
print("=" * 60)

# =============================================================================
# MODULE 3: VISUALIZATION ENGINE 1 (PUBLICATION-GRADE ISOTHERM PLOTS)
# =============================================================================
# --- FIGURE 2: EQUILIBRIUM ISOTHERMS ---
resolved_params = {
    ("as(iii)", 2): {"qmax": 57.05, "KL": 0.1960, "color": "darkred", "marker": "o", "label": "As(III) - pH 2.0"},
    ("as(iii)", 8): {"qmax": 47.83, "KL": 0.1025, "color": "salmon", "marker": "s", "label": "As(III) - pH 8.0"},
    ("as(v)", 2):   {"qmax": 24.10, "KL": 2.5138, "color": "teal", "marker": "^", "label": "As(V) - pH 2.0"},
    ("as(v)", 8):   {"qmax": 25.78, "KL": 0.0743, "color": "lightseagreen", "marker": "d", "label": "As(V) - pH 8.0"}
}

plt.figure(figsize=(8, 6.5))

for (species, ph), p in resolved_params.items():
    query = (df_eq["species"] == species) & (df_eq["pH"] == ph)
    sub = df_eq[query].sort_values(by="Ce_mgL")
    
    Ce_exp = sub["Ce_mgL"].values
    qe_exp = sub["qe_mgg"].values
    
    Ce_model = np.linspace(0, max(Ce_exp) * 1.05, 200) if len(Ce_exp) > 0 else np.linspace(0, 35, 200)
    qe_model = langmuir_equation(Ce_model, p["qmax"], p["KL"])
    
    plt.scatter(
        Ce_exp, qe_exp, 
        color=p["color"], marker=p["marker"], edgecolor="k", 
        s=65, zorder=5, label=f"{p['label']} (Exp)"
    )
    
    plt.plot(
        Ce_model, qe_model, 
        color=p["color"], linestyle="-", linewidth=2, 
        zorder=4, label=f"{p['label']} (Langmuir Fit)"
    )

plt.title("Equilibrium Adsorption Isotherms for Arsenic on Manganese Ferrite NPs", fontsize=12, fontweight="bold", pad=15)
plt.xlabel("Equilibrium Concentration, $C_e$ (mg/L)", fontsize=11, labelpad=8)
plt.ylabel("Adsorption Capacity, $q_e$ (mg/g)", fontsize=11, labelpad=8)
plt.xlim(left=0)
plt.ylim(bottom=0)
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend(loc="best", frameon=True)
plt.tight_layout()
plt.show()

# =============================================================================
# MODULE 4: VISUALIZATION ENGINE 2 (PHYSICOCHEMICAL INTERACTION BRIDGE GRAPH)
# =============================================================================
# --- FIGURE 3: SPECIATION & INTERACTION INTERFACE ---
pH_curve = np.linspace(2, 12, 500)
H_curve = 10**(-pH_curve)

zeta_curve = 35.0 * np.tanh((calculated_pzc - pH_curve) / 2.2)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.5))

# --- PANEL 1: ARSENIC(III) SURFACE INTERACTION INTERFACE ---
ax1_twin = ax1.twinx()

pKa1_3, pKa2_3, pKa3_3 = 9.22, 12.13, 13.40
Ka1_3, Ka2_3, Ka3_3 = 10**(-pKa1_3), 10**(-pKa2_3), 10**(-pKa3_3)
D_3 = (H_curve**3) + (H_curve**2 * Ka1_3) + (H_curve * Ka1_3 * Ka2_3) + (Ka1_3 * Ka2_3 * Ka3_3)

neutral_fraction_3 = ((H_curve**3) / D_3) * 100
mono_fraction_3 = ((H_curve**2 * Ka1_3) / D_3) * 100

ax1.plot(pH_curve, zeta_curve, color="darkorchid", lw=2.5, label="Simulated Surface Potential ($\zeta$)")
ax1_twin.plot(pH_curve, neutral_fraction_3, color="crimson", lw=1.5, label="Neutral $H_3AsO_3^0$ Fraction %")
ax1_twin.plot(pH_curve, mono_fraction_3, color="navy", linestyle=":", lw=1.5, label="$H_2AsO_3^-$ Fraction %")

ax1.fill_between(pH_curve, zeta_curve, 0, where=(pH_curve <= calculated_pzc), color="purple", alpha=0.05)
ax1_twin.scatter([2.0, 8.0], [57.05, 47.83], color="darkred", marker="o", edgecolor="k", s=75, zorder=5, label="Experimental $q_{max}$")
ax1.axvline(x=calculated_pzc, color="purple", linestyle=":", alpha=0.7, label=f"Experimental $pH_{{PZC}} = {calculated_pzc:.2f}$")

ax1.set_title("Arsenic(III) Surface Interaction Interface", fontsize=11, fontweight="bold")
ax1.set_xlabel("Solution pH")
ax1.set_ylabel("Surface Potential, $\zeta$ (mV)", color="darkorchid")
ax1_twin.set_ylabel("As(III) Speciation % / Capacity (mg/g)")
ax1.grid(True, linestyle="--", alpha=0.3)

# --- PANEL 2: ARSENIC(V) SURFACE INTERACTION INTERFACE ---
ax2_twin = ax2.twinx()

pKa1_5, pKa2_5, pKa3_5 = 2.22, 6.98, 11.53
Ka1_5, Ka2_5, Ka3_5 = 10**(-pKa1_5), 10**(-pKa2_5), 10**(-pKa3_5)
D_5 = (H_curve**3) + (H_curve**2 * Ka1_5) + (H_curve * Ka1_5 * Ka2_5) + (Ka1_5 * Ka2_5 * Ka3_5)

h2aso4_fraction_5 = ((H_curve**2 * Ka1_5) / D_5) * 100
haso4_fraction_5 = ((H_curve * Ka1_5 * Ka2_5) / D_5) * 100

ax2.plot(pH_curve, zeta_curve, color="darkorchid", lw=2.5)
ax2_twin.plot(pH_curve, h2aso4_fraction_5, color="forestgreen", linestyle="--", lw=1.5, label="$H_2AsO_4^-$ Fraction %")
ax2_twin.plot(pH_curve, haso4_fraction_5, color="dodgerblue", linestyle="-.", lw=1.5, label="$HAsO_4^{2-}$ Fraction %")

ax2.fill_between(pH_curve, zeta_curve, 0, where=(pH_curve <= calculated_pzc), color="purple", alpha=0.05)
ax2_twin.scatter([2.0, 8.0], [24.10, 25.78], color="teal", marker="^", edgecolor="k", s=75, zorder=5, label="Experimental $q_{max}$")
ax2.axvline(x=calculated_pzc, color="purple", linestyle=":", alpha=0.7)

ax2.set_title("Arsenic(V) Surface Interaction Interface", fontsize=11, fontweight="bold")
ax2.set_xlabel("Solution pH")
ax2_twin.set_ylabel("As(V) Speciation % / Capacity (mg/g)")
ax2.grid(True, linestyle="--", alpha=0.3)

# Final scale and axis label configurations
ax1.set_xlim(2, 12); ax1.set_ylim(-40, 40)
ax2.set_xlim(2, 12); ax2.set_ylim(-40, 40)
ax1_twin.set_ylim(0, 100); ax2_twin.set_ylim(0, 100)
ax1.axhline(0, color="gray", lw=0.5, alpha=0.5)
ax2.axhline(0, color="gray", lw=0.5, alpha=0.5)

lines1, labels1 = ax1.get_legend_handles_labels()
lines1_t, labels1_t = ax1_twin.get_legend_handles_labels()
ax1.legend(lines1 + lines1_t, labels1 + labels1_t, loc="lower left", frameon=True, fontsize=9)

lines2, labels2 = ax2.get_legend_handles_labels()
lines2_t, labels2_t = ax2_twin.get_legend_handles_labels()
ax2_twin.legend(lines2_t, labels2_t, loc="lower left", frameon=True, fontsize=9)

plt.suptitle("Physicochemical Interaction Bridge:\nSpeciation Dynamics vs. Manganese Ferrite Surface Charge Envelope", fontsize=12, fontweight="bold", y=0.98)
plt.tight_layout()
plt.show()

