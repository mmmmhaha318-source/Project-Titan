#!/bin/bash
TARGET=$1
RECON_DIR="results/$TARGET/recon"
VULN_DIR="results/$TARGET/vuln_scan"
mkdir -p $VULN_DIR
echo "[TITAN] Basic vulnerability scan initiated for $TARGET..."
nuclei -l $RECON_DIR/live_hosts.txt -t "technologies,cves,misconfiguration,vulnerabilities" -o $VULN_DIR/nuclei_findings.txt
echo "[TITAN] Basic vulnerability scan completed for $TARGET."
