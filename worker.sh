#!/bin/bash

################################################################################
# Vibe Coder - Worker Script
#
# The actual execution loop. Generates 1 app every 4 hours.
# Gets monitored by supervisor.sh
#
# Usage: ./worker.sh
################################################################################

set -e

# Configuration
WORK_DIR="${WORK_DIR:-$(dirname "$(readlink -f "$0")")}"
LOG_DIR="${WORK_DIR}/.vibe-loop"
HEARTBEAT_FILE="${LOG_DIR}/worker.heartbeat"
OUTPUT_FILE="${LOG_DIR}/worker.output"
ERROR_FILE="${LOG_DIR}/worker.error"
PID_FILE="${LOG_DIR}/worker.pid"
STATE_DIR="${WORK_DIR}/state"

# Create directories if needed
mkdir -p "$LOG_DIR"
mkdir -p "$STATE_DIR"

# Write PID file so supervisor can track us
echo $$ > "$PID_FILE"

################################################################################
# Main Loop
################################################################################

echo "[$(date)] Worker starting..."

while : do
  TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
  TIMESTAMP_ISO=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  
  echo "[$TIMESTAMP] Executing vibe coding cycle..."
  
  # Execute the vibe coder cycle
  OUTPUT=$(
    cd "$WORK_DIR"
    python3 vibe_coder.py run --max-ideas 5 2>&1
  )
  
  EXIT_CODE=$?
  
  # Write output
  {
    echo "=== Execution at $TIMESTAMP_ISO ==="
    echo "$OUTPUT"
    echo "Exit Code: $EXIT_CODE"
    echo ""
  } >> "$OUTPUT_FILE"
  
  # Write heartbeat (this is how supervisor knows we're alive)
  echo "$TIMESTAMP_ISO" > "$HEARTBEAT_FILE"
  
  # Save cycle state
  echo "$TIMESTAMP_ISO" > "${STATE_DIR}/last_cycle.txt"
  
  # If error, log it
  if [ $EXIT_CODE -ne 0 ]; then
    {
      echo "=== ERROR at $TIMESTAMP_ISO ==="
      echo "Exit Code: $EXIT_CODE"
      echo ""
    } >> "$ERROR_FILE"
    
    echo "[$TIMESTAMP] ERROR: Execution failed with code $EXIT_CODE"
  else
    echo "[$TIMESTAMP] Success. Next cycle in 4 hours."
  fi
  
  # Sleep 4 hours (14400 seconds)
  sleep 14400
done
