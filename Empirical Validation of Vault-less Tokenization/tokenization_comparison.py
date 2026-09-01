import time
import random
import string
import pandas as pd
import matplotlib.pyplot as plt
import pyffx

# ==========================================
# 1. DATA GENERATION (Synthetic PANs)
# ==========================================
def generate_synthetic_data(num_records=449):
    """Generates synthetic Visa-style PANs matching Sugumar (2025) design."""
    data = []
    for i in range(num_records):
        pan = '4' + ''.join([str(random.randint(0, 9)) for _ in range(15)])
        name = f"User_{random.choice(['Ahmed', 'Mohamed', 'Ali', 'Sara', 'Nour'])}_{i}"
        amount = round(random.uniform(10.0, 500.0), 2)
        merchant_id = f"MID_{random.randint(1000, 9999)}"
        data.append((pan, name, amount, merchant_id))
    return data

synthetic_transactions = generate_synthetic_data()
print(f"✅ Generated {len(synthetic_transactions)} synthetic transactions.")

# Save to CSV for reproducibility
df_data = pd.DataFrame(synthetic_transactions, columns=['PAN', 'Name', 'Amount', 'MerchantID'])
df_data.to_csv('synthetic_data.csv', index=False)
print("💾 Saved synthetic_data.csv")

# ==========================================
# 2. TOKENIZATION METHODS
# ==========================================

# --- Method A: Vault-Based Simulation (In-Memory Dictionary) ---
vault_db = {}

def vault_tokenization(pan):
    start = time.time()
    token = ''.join([str(random.randint(0, 9)) for _ in range(16)])
    vault_db[token] = pan  # Simulates DB write
    end = time.time()
    return token, (end - start) * 1000

# --- Method B: Vault-less FPE (Our Contribution) ---
fpe_key = b'0123456789abcdef0123456789abcdef'
cipher_fpe = pyffx.String(fpe_key, alphabet='0123456789', length=16)

def fpe_tokenization(pan):
    start = time.time()
    token = cipher_fpe.encrypt(pan)
    end = time.time()
    return token, (end - start) * 1000

# ==========================================
# 3. BENCHMARKING (Full Dataset)
# ==========================================
results_vault = []
results_fpe = []
tokens_fpe = []

print(" Running benchmark on full 449 records...")
for i in range(len(synthetic_transactions)):
    pan = synthetic_transactions[i][0]
    
    _, t_vault = vault_tokenization(pan)
    results_vault.append(t_vault)
    
    t_fpe, _ = fpe_tokenization(pan)
    results_fpe.append(t_fpe)
    tokens_fpe.append(t_fpe)

avg_vault = sum(results_vault) / len(results_vault)
avg_fpe = sum(results_fpe) / len(results_fpe)

# Reversibility Check
test_pan = synthetic_transactions[0][0]
recovered = cipher_fpe.decrypt(tokens_fpe[0])
is_reversible = (test_pan == recovered)

# Format Preservation Check
format_preserved = all(len(t) == 16 and t.isdigit() and t.startswith('4') for t in tokens_fpe)

# ==========================================
# 4. RESULTS & VISUALIZATION
# ==========================================
print(f"\n📊 RESULTS:")
print(f"Vault-based Avg Latency: {avg_vault:.4f} ms")
print(f"FPE Avg Latency:         {avg_fpe:.4f} ms")
print(f"Reversibility:           {is_reversible}")
print(f"Format Preserved:        {format_preserved}")

# Plotting
plt.figure(figsize=(10, 6))
methods = ['Vault-based\n(Simulated)', 'FF1 FPE\n(Vault-less)']
latencies = [avg_vault, avg_fpe]
colors = ['#3498db', '#e74c3c']
bars = plt.bar(methods, latencies, color=colors, edgecolor='black')

for bar, val in zip(bars, latencies):
    plt.text(bar.get_x() + bar.get_width()/2., val, 
             f'{val:.4f} ms', ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.title('Performance Comparison: Vault vs FPE Tokenization', fontsize=16)
plt.ylabel('Average Latency (ms)', fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('latency_comparison.png', dpi=300)
plt.show()
print("💾 Saved latency_comparison.png")