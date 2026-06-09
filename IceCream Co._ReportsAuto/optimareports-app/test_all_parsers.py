import os
import traceback
from parser import parse_franchise

xlsx_files = [
    ('betafranchise.xlsx', 'BetaFranchise', 'Abril 2026'),
    ('betafranchise APRIL.xlsx', 'BetaFranchise', 'Abril 2026'),
    ('GammaFranchise APRIL.xlsx', 'GammaFranchise', 'Abril 2026'),
    ('deltafranchise April.xlsx', 'DeltaFranchise', 'Abril 2026'),
    ('alphafranchise APRIL.xlsx', 'AlphaFranchise', 'Abril 2026'),
    ('March_gammafranchise.xlsx', 'GammaFranchise', 'Marzo 2026'),
    ('March_DeltaFranchise.xlsx', 'DeltaFranchise', 'Marzo 2026'),
    ('March_alphafranchise.xlsx', 'AlphaFranchise', 'Marzo 2026'),
]

for filename, franchise, period in xlsx_files:
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), filename)
    if not os.path.exists(path):
        print(f"Skipping {filename} (not found at {path})")
        continue
    try:
        data = parse_franchise(path, franchise, period, f'01 – 30 {period}')
        print(f"SUCCESS: {filename} parsed successfully!")
    except Exception as e:
        print(f"FAILED: {filename} failed to parse!")
        traceback.print_exc()
