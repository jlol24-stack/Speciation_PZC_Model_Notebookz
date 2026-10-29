# Mechanistic Adsorption Engine for Arsenic Speciation on Manganese Ferrite Nano-Adsorbents
## Computational Framework for Surface Potential Dynamics & Non-Linear Isotherm Regression

This repository contains the Python-based data processing, non-linear regression analysis, and visualization pipelines developed to model the competitive uptake of toxic oxyanions ($\text{As(III)}$ and $\text{As(V)}$) utilizing synthetic manganese ferrite nano-adsorbents.

---

### 🔬 Project Context & Credits

**Authors:** López‑Luna, J.$^{1*}$, Martinez-Vargas, S.$^{2}$, Martínez I.A.$^{3}$, Hernández-Beteta, E.E.$^{4}$, Mijangos-Ricardez, O.F.$^{4}$, Vázquez-Hipólito, V.$^{5}$, Patiño-Carachure, C.$^{2}$

$^{1}$ Independent Researcher; $^{2}$ Universidad Autónoma del Carmen, Campeche, México; $^{3}$ Cinvestav, Saltillo, México; $^{4}$ Universidad de la Sierra Juárez, Oaxaca, México; $^{5}$ Universidad Tecnológica de la Mixteca, Oaxaca, México.  
$^{*}$ **Corresponding author:** jlol_24@hotmail.com
**DOI:** 10.5281/zenodo.23745235


#### Original Reference Study
The core experimental framework, raw datasets, and primary kinetic models utilized as the baseline for this project were originally published in:
* Martinez–Vargas, S., Martínez, A. I., Hernández–Beteta, E. E., Mijangos–Ricardez, O. F., Vázquez–Hipólito, V., Patiño-Carachure, C., & López–Luna, J. (2018). *As(III) and As(V) adsorption on manganese ferrite nanoparticles*. **Journal of Molecular Structure**, Volume 1154, Pages 524-534.  
* **DOI:** [10.1016/j.molstruc.2017.10.076](https://doi.org)

---

### 📌 Project Executive Summary

The computational architecture implements four distinct mathematical modules in a single pipeline:

1. **Module 1 (pH_PZC):** Resolving the Point of Zero Charge ($\text{pH}_{\text{PZC}}$) using univariate spline root extraction ($f(\text{pH}_i) = \text{pH}_f - \text{pH}_i = 0$).
2. **Module 2 (Equilibrium Regression):** Non-linear parameter optimization using the Langmuir adsorption isotherm expression via Levenberg-Marquardt regression.
3. **Module 3 (Isotherm Analytics):** Publication-grade visualization mapping experimental matrices against empirical thermodynamic models.
4. **Module 4 (Physicochemical Interaction Bridge):** Dual-axis speciation mapping evaluating oxyanion protonation states relative to the nanoparticle surface potential charge envelope ($\zeta$).

---

### 🛠️ Execution Requirements

#### Required Datasets
The script requires the following two raw Excel spreadsheet files placed within the same workspace directory:
* `pzc_Mn_ferrite.xlsx` — Experimental initial vs. final pH data matrices.
* `dataeq_speciation.xlsx` — Raw equilibrium adsorption and concentration vectors.

#### Core Dependencies
Install the required scientific stack via terminal or your environments manager:
```bash
pip install numpy pandas matplotlib scipy openpyxl
```
