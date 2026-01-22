import numpy as np
import pandas as pd

np.random.seed(42)

# Time range: 7 days, 1-min interval
timestamps = pd.date_range(
    start="2026-01-01",
    periods=7 * 24 * 60,
    freq="1min"
)

# Simulate traffic
rps = np.random.poisson(lam=120, size=len(timestamps))

# Infra metrics
cpu = np.clip(rps * 0.35 + np.random.normal(0, 5, len(rps)), 10, 100)
memory = np.clip(cpu * 0.9 + np.random.normal(0, 4, len(cpu)), 20, 100)

# Latency behavior (non-linear)
latency = 80 + (cpu ** 1.4) + np.random.normal(0, 20, len(cpu))

# Error rate increases after SLA breach
error_rate = np.where(
    latency > 300,
    np.random.uniform(1, 5, len(latency)),
    np.random.uniform(0, 0.5, len(latency))
)

df = pd.DataFrame({
    "timestamp": timestamps,
    "rps": rps,
    "cpu_usage": cpu,
    "memory_usage": memory,
    "latency_ms": latency,
    "error_rate": error_rate
})

df.to_csv("data/raw/api_metrics.csv", index=False)
print("✅ Synthetic dataset generated successfully")
