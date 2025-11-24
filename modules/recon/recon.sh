#!/bin/bash
TARGET=$1
RESULT_DIR="results/$TARGET"
SUBDOMAIN_FILE="$RESULT_DIR/subdomains.txt"
LIVE_HOSTS_FILE="$RESULT_DIR/live_hosts.txt"

echo "=================================================="
echo "Starting Recon Module for: $TARGET"
echo "=================================================="

echo "[*] Running subfinder for subdomains..."
subfinder -d $TARGET -o $SUBDOMAIN_FILE -silent

echo "[*] Running httpx to find live web servers..."
httpx -l $SUBDOMAIN_FILE -o $LIVE_HOSTS_FILE -silent -threads 100

echo "[+] Recon Module finished for $TARGET."
