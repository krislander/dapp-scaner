#!/bin/bash
# Run all DApp ecosystem analyses

# Always run from the script's own directory
cd "$(dirname "$0")" || exit 1

echo "================================"
echo "Running All DApp Analyses"
echo "================================"
echo ""

source ../.venv/bin/activate

echo "[1/9] Data Preparation..."
python 01_data_preparation.py

echo ""
echo "[2/9] Governance Analysis..."
python 02_governance_analysis.py

echo ""
echo "[3/9] Ecosystem Analysis..."
python 03_ecosystem_analysis.py

echo ""
echo "[4/9] Market Analysis..."
python 04_market_analysis.py

echo ""
echo "[5/9] Adoption Analysis..."
python 05_adoption_analysis.py

echo ""
echo "[6/9] Performance Analysis..."
python 06_performance_analysis.py

echo ""
echo "[7/9] Funding Analysis..."
python 07_funding_analysis.py

echo ""
echo "[8/9] Category Comparison..."
python 08_category_comparison.py

echo ""
echo "[9/9] Key Insights..."
python 09_key_insights.py

echo ""
echo "================================"
echo "All Analyses Complete!"
echo "================================"
echo "Results saved to: outputs/"
