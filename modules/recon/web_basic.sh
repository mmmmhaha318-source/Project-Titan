#!/bin/bash
TARGET=$1
RESULTS_DIR="results/$TARGET/recon"
mkdir -p $RESULTS_DIR
echo "[TITAN] Basic web recon initiated for $TARGET..."
subfinder -d $TARGET -o $RESULTS_DIR/subdomains.txt
httpx -l $RESULTS_DIR/subdomains.txt -o $RESULTS_DIR/live_hosts.txt
echo "[TITAN] Basic web recon completed for $TARGET."
