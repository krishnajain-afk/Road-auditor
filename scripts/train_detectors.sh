#!/usr/bin/env bash
# Train the CFI damage (pothole) and Indian traffic-sign detectors with ultralytics (CPU or GPU).
# Resumes automatically if a previous run was interrupted.
set -e
cd "$(dirname "$0")/.."
source .venv/bin/activate
export OMP_NUM_THREADS=${OMP_NUM_THREADS:-3}
DEV=${DEVICE:-cpu}
P=runs/detect/runs/pothole; S=runs/detect/runs/itsd
if [ -f $P/weights/last.pt ] && [ ! -f data/models/cfi_damage.pt ]; then
  yolo detect train resume model=$P/weights/last.pt || true
elif [ ! -f data/models/cfi_damage.pt ]; then
  yolo detect train data=data/datasets/pothole/data.yaml model=data/models/yolov8n.pt imgsz=${IMGSZ:-480} epochs=${EPOCHS:-30} batch=16 device=$DEV workers=2 project=runs name=pothole exist_ok=True patience=10 plots=False verbose=False
fi
[ -f $P/weights/best.pt ] && cp $P/weights/best.pt data/models/cfi_damage.pt
if [ -f $S/weights/last.pt ] && [ ! -f data/models/cfi_signs.pt ]; then
  yolo detect train resume model=$S/weights/last.pt || true
elif [ ! -f data/models/cfi_signs.pt ]; then
  yolo detect train data=data/datasets/itsd/data.yaml model=data/models/yolov8n.pt imgsz=${IMGSZ:-480} epochs=${EPOCHS_SIGN:-40} batch=16 device=$DEV workers=2 project=runs name=itsd exist_ok=True patience=15 plots=False verbose=False
fi
[ -f $S/weights/best.pt ] && cp $S/weights/best.pt data/models/cfi_signs.pt
echo TRAINING_DONE
