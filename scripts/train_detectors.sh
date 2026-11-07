#!/usr/bin/env bash
# Train the CFI damage (pothole) and Indian traffic-sign detectors on CPU/GPU with ultralytics.
set -e
cd "$(dirname "$0")/.."
source .venv/bin/activate
export OMP_NUM_THREADS=${OMP_NUM_THREADS:-3}
DEV=${DEVICE:-cpu}
yolo detect train data=data/datasets/pothole/data.yaml model=data/models/yolov8n.pt imgsz=${IMGSZ:-480} epochs=${EPOCHS:-30} batch=16 device=$DEV workers=2 project=runs name=pothole exist_ok=True patience=10 plots=False verbose=False
cp runs/pothole/weights/best.pt data/models/cfi_damage.pt
yolo detect train data=data/datasets/itsd/data.yaml model=data/models/yolov8n.pt imgsz=${IMGSZ:-480} epochs=${EPOCHS_SIGN:-40} batch=16 device=$DEV workers=2 project=runs name=itsd exist_ok=True patience=15 plots=False verbose=False
cp runs/itsd/weights/best.pt data/models/cfi_signs.pt
echo TRAINING_DONE
