# bikenv: Environmental factors that affect cycling

Topographical and climatic indexes to quantify their effect on cycling.

## Project Structure

This is a research analysis project, not a Python package. The structure is:

- `scripts/` - Core calculation functions (altitude_index, distance_index)
- `analysis/` - Statistical analysis and hypothesis testing platform
- `data/` - Copenhagenize Index 2025 Edition reference data
- `results/` - Generated analysis outputs (CSV, plots)
- `requirements-platform.txt` - Python dependencies

**Note:** This project was previously structured as an installable package with `setup.py` and a `bikenv/` module, but has been refactored into a scripts-based analysis platform. All dependencies are managed via `requirements-platform.txt`.