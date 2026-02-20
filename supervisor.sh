#!/bin/bash

################################################################################
# Vibe Coder - Supervisor Script
#
# Monitors the worker process and restarts it if it fails.
# Uses Ralph Loop supervisor/worker architecture.
#
# Usage: ./supervisor.sh
################################################################################

set -e

# Configuration
WORK_DIR="${WORK_DIR:-$(dirname "$(readlink -f "$0")")}"
LOG_DIR="${WORK_DIR}/.vibe-loop"
HEARTBEAT_FILE="${LOG_DIR}/worker.heartbeat"
OUTPUT_FILE="${LOG_DIR}/worker.output"
ERROR_FILE="${LOG_DIR}/worker.error"
PID_FILE="${LOG_DIR}/worker.pid"
RESTART_COUNT_FILE="${LOG_DIR}/restart_count"
SUPERVISOR_LOG="${LOG_DIR}/supervisor.log"

# Timing (in seconds)
CHECK_INTERVAL=3600       # Check every 1 hour
HEARTBEAT_TIMEOUT=16200   # 4.5 hours (worker should heartbeat every 4 hours)
MAX_RESTARTS=3

# Create directories if needed
mkdir -p "$LOG_DIR"

################################################################################
# Helper Functions
################################################################################

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$SUPERVISOR_LOG"
}

get_pid() {
  if [ -f "$PID_FILE" ]; then
    cat "$PID_FILE"
  else
    echo ""
  fi
}

is_process_running() {
  local pid="$1"
  if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
    return 0
  else
    return 1
  fi
}

get_heartbeat_age() {
  if [ -f "$HEARTBEAT_FILE" ]; then
    local last_heartbeat=$(cat "$HEARTBEAT_FILE")
    local last_timestamp=$(date -d "$last_heartbeat" +%s 2>/dev/null || echo 0)
    local now=$(date +%s)
    echo $((now - last_timestamp))
  else
    echo 999999
  fi
}

get_restart_count() {
  if [ -f "$RESTART_COUNT_FILE" ]; then
    cat "$RESTART_COUNT_FILE"
  else
    echo 0
  fi
}

increment_restart_count() {
  local count=$(get_restart_count)
  count=$((count + 1))
  echo "$count" > "$RESTART_COUNT_FILE"
  echo "$count"
}

reset_restart_count() {
  echo 0 > "$RESTART_COUNT_FILE"
}

start_worker() {
  log "Starting worker process..."
  
  # Start worker in background
  nohup bash "$WORK_DIR/worker.sh" > /dev/null 2>&1 &
  local worker_pid=$!
  
  log "Worker started with PID: $worker_pid"
  
  # Wait a moment for worker to initialize
  sleep 5
  
  # Verify it started
  if is_process_running "$worker_pid"; then
    log "Worker is running"
    return 0
  else
    log "ERROR: Worker failed to start"
    return 1
  fi
}

stop_worker() {
  local pid=$(get_pid)
  
  if [ -n "$pid" ] && is_process_running "$pid"; then
    log "Stopping worker (PID: $pid)..."
    kill "$pid" 2>/dev/null || true
    
    # Wait for process to stop
    for i in {1..10}; do
      if ! is_process_running "$pid"; then
        log "Worker stopped"
        return 0
      fi
      sleep 1
    done
    
    # Force kill if still running
    kill -9 "$pid" 2>/dev/null || true
    log "Worker force killed"
  fi
}

diagnose_failure() {
  log "DIAGNOSING: Reading last output..."
  
  # Read last 50 lines of output
  if [ -f "$OUTPUT_FILE" ]; then
    local last_output=$(tail -50 "$OUTPUT_FILE")
    log "Last output:\n$last_output"
  fi
  
  # Read last errors
  if [ -f "$ERROR_FILE" ]; then
    local last_errors=$(tail -20 "$ERROR_FILE")
    log "Last errors:\n$last_errors"
  fi
  
  # Try to diagnose with AI if qwen-code is available
  if command -v qwen-code &> /dev/null; then
    log "Asking AI to diagnose..."
    
    local diagnosis=$(qwen-code -p "
Here's the last output from a failed vibe-coder worker:
$(tail -50 "$OUTPUT_FILE" 2>/dev/null || echo 'No output')

Here are the errors:
$(tail -20 "$ERROR_FILE" 2>/dev/null || echo 'No errors')

What went wrong? Provide a brief diagnosis in 2-3 sentences.
" 2>/dev/null || echo "Unable to get AI diagnosis")
    
    log "DIAGNOSIS: $diagnosis"
  else
    log "DIAGNOSIS: Manual inspection required (qwen-code not available)"
  fi
}

################################################################################
# Main Supervisor Loop
################################################################################

log "========================================="
log "Vibe Coder Supervisor Starting"
log "========================================="
log "Check interval: ${CHECK_INTERVAL}s"
log "Heartbeat timeout: ${HEARTBEAT_TIMEOUT}s"
log "Max restarts: ${MAX_RESTARTS}"
log "========================================="

# Check if worker is already running
existing_pid=$(get_pid)
if is_process_running "$existing_pid"; then
  log "Worker already running (PID: $existing_pid)"
else
  log "No worker running, starting initial worker..."
  start_worker || exit 1
  reset_restart_count
fi

# Main monitoring loop
while : do
  # Wait for check interval
  log "Checking worker status..."
  
  # Get worker status
  current_pid=$(get_pid)
  heartbeat_age=$(get_heartbeat_age)
  restart_count=$(get_restart_count)
  
  # Check if worker is running
  worker_running=false
  if is_process_running "$current_pid"; then
    worker_running=true
  fi
  
  # Check if heartbeat is fresh
  heartbeat_fresh=false
  if [ "$heartbeat_age" -lt "$HEARTBEAT_TIMEOUT" ]; then
    heartbeat_fresh=true
  fi
  
  # Log status
  log "Worker PID: ${current_pid:-none}"
  log "Worker running: $worker_running"
  log "Heartbeat age: ${heartbeat_age}s"
  log "Heartbeat fresh: $heartbeat_fresh"
  log "Restart count: $restart_count"
  
  # Determine if worker needs restart
  needs_restart=false
  reason=""
  
  if [ "$worker_running" = false ]; then
    needs_restart=true
    reason="Worker process not running"
  elif [ "$heartbeat_fresh" = false ]; then
    needs_restart=true
    reason="Heartbeat stale (${heartbeat_age}s > ${HEARTBEAT_TIMEOUT}s)"
  fi
  
  if [ "$needs_restart" = true ]; then
    log "ALERT: $reason"
    
    # Check restart count
    if [ "$restart_count" -ge "$MAX_RESTARTS" ]; then
      log "CRITICAL: Max restarts exceeded ($MAX_RESTARTS)"
      log "CRITICAL: Manual intervention required"
      log "========================================="
      log "SUPERVISOR EXITING IN FAILED STATE"
      log "========================================="
      exit 1
    fi
    
    # Diagnose failure
    diagnose_failure
    
    # Stop old worker (if still running)
    stop_worker
    
    # Increment restart count
    new_count=$(increment_restart_count)
    log "Incrementing restart count to: $new_count"
    
    # Start new worker
    start_worker
    
    if [ $? -eq 0 ]; then
      log "Worker restarted successfully"
    else
      log "ERROR: Failed to restart worker"
    fi
  else
    log "Worker status: OK"
    
    # Reset restart count on successful run
    if [ "$restart_count" -gt 0 ]; then
      reset_restart_count
      log "Reset restart count (worker running successfully)"
    fi
  fi
  
  log "Next check in ${CHECK_INTERVAL}s"
  log "-----------------------------------------"
  
  # Sleep until next check
  sleep "$CHECK_INTERVAL"
done
