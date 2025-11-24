#!/bin/bash
TARGET=$1
RESULT_DIR="results/$TARGET"
NUCLEI_OUTPUT_FILE="$RESULT_DIR/nuclei_raw.txt"

echo "=================================================="
echo "Starting AI Analysis & Reporting Module for: $TARGET"
echo "=================================================="

FINDINGS=$(cat $NUCLEI_OUTPUT_FILE)

# Generate AI Summary
AI_SUMMARY=$(python3 core/ai_analyzer.py "$FINDINGS")
echo "[*] AI Summary Generated."

# Send Discord Notification
python3 core/discord_notifier.py "$TARGET" "$AI_SUMMARY" "$FINDINGS"
echo "[*] Discord notification sent."

# Generate PDF/Markdown Report
python3 core/pdf_generator.py "$TARGET" "$AI_SUMMARY" "$NUCLEI_OUTPUT_FILE"
echo "[*] Markdown report file generated."

echo "[+] AI Analysis & Reporting Module finished for $TARGET."
