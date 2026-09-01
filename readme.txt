# Empirical Validation of Vault-less Tokenization: Code & Results Artifact

## Overview
This repository contains the Python implementation and experimental results for the paper **"Empirical Validation of Vault-less Tokenization: A Performance and Architectural Comparison with Vault-based Systems for PCI DSS Compliance"**. 

It provides the first measured, head-to-head comparison between a traditional Vault-based tokenization baseline and a NIST FF1 Format-Preserving Encryption (FPE) vault-less scheme, closing the empirical gap left open by Sugumar (2025) and subsequent extension proposals [1], [2], [3].

## Key Contributions Validated by This Code
1. **Working FPE Implementation**: A functional vault-less tokenization engine using `pyffx` (NIST SP 800-38G FF1).
2. **Direct Latency Benchmarking**: Measured performance on 449 synthetic PANs under matched conditions.
3. **Format Preservation Proof**: Verified 100% reversibility and identical output format (16-digit numeric) to legacy PANs.
4. **Transparent Limitation Disclosure**: Explicit documentation of the in-memory dictionary simulation vs. production MySQL reality.

## Experimental Setup
- **Environment**: Google Colab (Python 3.x)
- **Dataset**: 449 synthetic Visa-style PANs (starting with '4'), generated programmatically to match [1].
- **Baseline (Vault)**: In-memory Python dictionary simulating token storage (isolates crypto cost from I/O).
- **Proposed (FPE)**: `pyffx.String(key, alphabet='0123456789', length=16)` for stateless encryption.
- **Metrics**: Average latency (ms), Reversibility (%), Format Preservation.

## How to Reproduce
1. Install dependencies: `pip install pyffx cryptography pandas matplotlib`
2. Run `tokenization_comparison.py` (or the provided Jupyter Notebook).
3. The script will generate 449 records, run both methods, and output Table 1 + Figure 1 automatically.

## Key Results Summary
| Method | Avg. Latency (ms) | DB Required | Format Preserved |
| :--- | :--- | :--- | :--- |
| Vault-based (Simulated) | 0.0117 | Yes (In-Memory Dict) | Random |
| FF1 FPE (Proposed) | 0.0864 | No (Stateless) | ✅ Same as PAN |

> **⚠️ Critical Note on Latency Ordering**: The simulated vault appears faster (0.01 ms) because it bypasses disk/network I/O. As documented in [1], real MySQL-backed vaults incur 50–70 ms latency. Our FPE overhead (~0.07 ms) is negligible compared to network latency and eliminates the single point of failure inherent to centralized vaults.

## File Structure
- `tokenization_comparison.py`: Main benchmarking script.
- `synthetic_data.csv`: Generated 449-record dataset (for reproducibility).
- `results/`: Output table (CSV) and latency chart (PNG).
- `requirements.txt`: Exact library versions used.

## References
[1] B. Sugumar, "Data Tokenization: A Key Enabler for PCI DSS Compliance," ICEET 2025.  
[2] "Comparative Analysis of Vaulted and Vault-less Tokenization..." (Extension Proposal).  
[3] "A Behavioral Anomaly-Detection Layer..." (Extension Study).  
[4] NIST SP 800-38G: Recommendation for Block Cipher Modes of Operation: FPE.