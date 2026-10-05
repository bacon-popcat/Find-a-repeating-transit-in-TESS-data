"""Saturday, step 1: download one TESS light curve and clean it.

Run with:  .venv\Scripts\python step1_download.py
"""
import lightkurve as lk

TARGET = "WASP-18"  # star with a known hot Jupiter, period about 0.941 days

# 1. Ask the MAST archive which TESS light curves exist for this star.
#    "SPOC" is the official TESS pipeline; 120 s means 2-minute cadence.
search = lk.search_lightcurve(TARGET, mission="TESS", author="SPOC", exptime=120)
print(search)  # a table listing each available sector

# 2. Download only the first sector to keep things simple.
lc = search[0].download()
print(f"\nDownloaded {len(lc)} points from sector {lc.sector}")

# 3. Clean: drop NaN (missing) values. Lightkurve already removes points whose
#    quality flags mark them as bad when it downloads with the default settings.
lc = lc.remove_nans()
print(f"After removing missing values: {len(lc)} points")

# 4. Normalize so the typical brightness equals 1.0 (a 1% dip then reads as 0.99).
lc = lc.normalize()
print(f"Time span: {lc.time.min().value:.2f} to {lc.time.max().value:.2f} (BTJD days)")
print(f"Mean flux after normalizing: {lc.flux.value.mean():.5f}")
