# Smart Feed Mill: prototype

> **Status: proposed idea and early prototype. Not a finished, deployed or validated system.**
> All data here is **synthetic**. No real company, supplier or laboratory data is used.

## The idea
Feed mills generate production, QC, inventory, maintenance and dispatch records every day, but much of it sits in registers and spreadsheets. The proposed system would connect these records, show the manager what needs attention, and keep safety stops as fixed rules rather than AI guesses.

This repo explores one small piece: **scoring incoming raw-material lots before the rapid aflatoxin result is known**, so QC can prioritise probing and sampling.

## What is in the repo
| Path | What it is |
|---|---|
| `data/generate_mock_data.py` | Generates 1,200 simulated lots (seeded, reproducible) |
| `data/mock_lots.csv` | Output of the script |
| `notebooks/risk_scoring.ipynb` | Feature building, time-based split, logistic regression, risk bands, hard-stop overlay |
| `requirements.txt` | Python dependencies |

## Design choices worth noting
- **No label leakage:** the rapid-test reading is not a feature.
- **Time-based split:** train on earlier lots, test on the latest 20%.
- **Supplier history** uses only earlier lots, smoothed toward the overall rate.
- **Hard stop stays a rule:** a positive rapid test always means HOLD. The score only sets sampling priority.

## Example result (synthetic data only)
On the held-out latest 20%, the model reached ROC AUC 0.80 against 0.74 for a moisture-only baseline. The highest risk band had a 61% positive rate and the lowest 9%.

**These numbers only show that the pipeline runs.** The data was generated from relationships I wrote myself, so the model is recovering my assumptions, not facts about real mills.

## Limitations
- Synthetic data; the 20 ppb threshold and band cut-offs are placeholders, not regulatory limits.
- A real version needs lot-level records from actual mills, permission to use them, and validation against QC outcomes.
- The score never overrides a test result or a QC hold.

## Run it
```bash
pip install -r requirements.txt
python data/generate_mock_data.py
jupyter notebook notebooks/risk_scoring.ipynb
```
