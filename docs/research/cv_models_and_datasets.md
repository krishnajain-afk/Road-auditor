# CFI Road Auditor — CV models, datasets, ingest & geometry research

*Research date: 2026-11-07. Author: ML/CV research pass for the CFI Road Auditor (automated Road Safety Audit for Indian roads).*

## 0. How to read this document, and the network reality

**Verification legend used throughout**

| Tag | Meaning |
|---|---|
| **[V]** | Verified on 2026-11-07 from this research sandbox: HTTP 200 with the stated byte size, sha256 computed on the downloaded file, and (for ONNX/ncnn) the file was loaded and run with `onnxruntime`/`ncnn` from PyPI. |
| **[V-pip]** | Wheel downloaded from PyPI and its contents listed (`unzip -l`). |
| **[P]** | Probed from the sandbox and **blocked** here (proxy `403`). The build machine's allow-list differs from the sandbox's, so treat as "test from the build box". |
| **[U]** | From literature/README/search only, not independently verified. |

**Host reachability matrix** (sandbox probe; build-machine column is what you told me)

| Host | Build machine (stated) | Sandbox probe | Notes |
|---|---|---|---|
| `pypi.org`, `files.pythonhosted.org` | reachable | reachable | Primary channel. |
| `raw.githubusercontent.com` | reachable | reachable | Serves files **committed** to a repo. **Git-LFS files come back as a 130-byte pointer, not the binary** (see §1.0 — this kills ~95 % of "weights in repo" candidates). |
| `github.com/<o>/<r>/releases/download/...` (actually served by `objects.githubusercontent.com`) | **blocked** | reachable | Ultralytics, YOLOPv2, HybridNets, MiDaS, EasyOCR, YOLOX all live here. sha256 hashes for these are in §6 so you can verify files once mirrored. |
| `api.github.com` | unknown | reachable | Needed only to *enumerate* repo trees (`/repos/{o}/{r}/git/trees/{branch}?recursive=1`). |
| `codeload.github.com` (repo zip) | unknown | blocked | |
| `huggingface.co`, `hf-mirror.com`, `modelscope.cn` | **blocked** | blocked | Depth-Anything, SegFormer, Mask2Former, timm, RDD HF models. |
| `download.pytorch.org` | **blocked** | blocked | torchvision / smp encoders. |
| `storage.googleapis.com` | unknown — **test this** | reachable | MediaPipe EfficientDet-Lite COCO detectors, Keras-Applications backbones. |
| `download.tensorflow.org`, `tfhub.dev`, `drive.google.com`, `download.openmmlab.com`, `paddle*.bcebos.com`, `storage.openvinotoolkit.org`, `jaided.ai`, `dl.fbaipublicfiles.com`, `sghub.deci.ai` | unknown | blocked | OpenMMLab, PaddleOCR/PaddleSeg, OpenVINO OMZ, SAM/Detectron2, SuperGradients. |
| `figshare.com`, `data.mendeley.com`, `zenodo.org`, `kaggle.com`, `ieee-dataport.org`, `universe.roboflow.com` | mostly **blocked** | blocked | Nearly every dataset host. |
| `bigdatacup.s3.ap-northeast-1.amazonaws.com`, `mycityreport.s3-ap-northeast-1.amazonaws.com` (RDD2022/2020 S3) | unknown | **S3 `AccessDenied` (dead), not a proxy block** | The sekilab README S3 links no longer serve; figshare is the surviving mirror. |
| `idd.insaan.iiit.ac.in`, `mobility.iiit.ac.in`, `bdd-data.berkeley.edu`, `dl.cv.ethz.ch`, `cityscapes-dataset.com`, `cvlibs.net`, `benchmark.ini.rub.de`, `sid.erda.dk`, `hci.iwr.uni-heidelberg.de`, `mapillary.com` | unknown | blocked | All gated/registration datasets. |

**Bottom line.** With *only* PyPI + raw.githubusercontent.com you can stand up: COCO-class detection and instance segmentation (YOLOv8n/YOLO11n ONNX & ncnn), YOLOP (drivable area + lane lines + vehicles), OCR (RapidOCR bundled PP-OCR models; tesseract traineddata), classical geometry (OpenCV), and Claude vision. You **cannot** get any pretrained pothole/RDD2022, Indian traffic-sign, crosswalk, speed-breaker, Cityscapes/Mapillary segmentation or monocular-depth model through those two channels — every such file I found on GitHub is a Git-LFS pointer. Those need the one-time "Tier B" bridge in §6.

---

## 1. Detection models per asset class

### 1.0 The Git-LFS trap (important, verified)

`raw.githubusercontent.com` returns the *committed blob*. When a repo stores a `.pt/.onnx` through Git LFS, the committed blob is a ~130-byte text pointer (`version https://git-lfs.github.com/spec/v1 …`); the real binary is on `media.githubusercontent.com` (blocked class). I HEAD-checked ~70 candidate weight files found via GitHub code search (pothole `best.pt`, `YOLOv8_Small_RDD.pt`, `rdd2022_yolov8.pt`, `zebra_crossing.pt`, `yolov8n_crosswalk_stopline.pt`, `traffic_sign_detector.pt`, `depth_anything_v2_vits.onnx`, `ufld_culane.onnx`, `yolov8n-seg.onnx`, etc.). **All of them returned `Content-Length: 131–134` → LFS pointers.** Also LFS: `opencv/opencv_zoo`, `onnx/models`. Rule of thumb: only trust a raw URL after a HEAD shows a plausible size (> 1 MB) — a check script is in §6.4.

Files that **are** real binaries on raw.githubusercontent.com (all [V], sha256 in §6.2):

| File | Size | License | What it is |
|---|---|---|---|
| `hustvl/YOLOP/main/weights/End-to-end.pth` | 95.8 MB | MIT | YOLOP PyTorch weights (vehicle det + drivable area + lane line seg, BDD100K) |
| `hustvl/YOLOP/main/weights/yolop-640-640.onnx` (also 320 & 1280 variants) | 35.9 MB | MIT | YOLOP ONNX; outputs `det_out (1,25200,6)`, `drive_area_seg (1,2,640,640)`, `lane_line_seg (1,2,640,640)`; **247 ms/frame on this 4-core CPU** |
| `Hyuto/yolov8-onnxruntime-web/master/public/model/yolov8n.onnx` | 12.8 MB | weights AGPL-3.0 (Ultralytics) | YOLOv8n COCO-80 detector; `(1,84,8400)`; **35 ms/frame CPU** |
| `Hyuto/yolov8-seg-onnxruntime-web/master/public/model/yolov8n-seg.onnx` | 13.8 MB | AGPL-3.0 | YOLOv8n-seg COCO instance seg; 48 ms/frame CPU |
| `Hyuto/yolov5-onnxruntime-web/master/public/model/yolov5n.onnx` (+ `yolov5-seg-…/yolov5n-seg.onnx`) | 7.9 / 8.4 MB | AGPL-3.0 | YOLOv5n COCO |
| `AndreyGermanov/yolov8_onnx_python/main/yolov8m.onnx` | 103.8 MB | repo GPL-3.0; weights AGPL-3.0 | YOLOv8m COCO (better recall on small objects); 176 ms/frame CPU |
| `nihui/ncnn-assets/master/models/yolov8n.ncnn.{param,bin}`, `yolo11n.ncnn.*`, `yolov8n_seg.ncnn.*`, `yolo11n_seg.ncnn.*`, `yolov8s_worldv2.ncnn.*`, `yolov7-tiny.*`, `yolov6n.*`, `yolov5s.*`, `nanodet_m.*`, `yolact.*`, `mobilenetv2_ssdlite_voc.*`, `mobilenetv3_ssdlite_voc.*`, `squeezenet_ssd_voc.*`, `mobilenetv2_yolov3.*` | 1.9–73 MB | per upstream model (YOLOv8/11 AGPL; YOLOv7 GPL; NanoDet/YOLOv6/yolact Apache/MIT) | ncnn format; run with `pip install ncnn` (loads: verified). `yolov8s_worldv2` is a YOLO-World export with a fixed (COCO) vocabulary. |
| `Qengineering/YoloV8-ncnn-Raspberry-Pi-4/main/yolov8n.{param,bin}`, `yolov8s.bin` | 6.3 / 22.3 MB | repo BSD-3; weights AGPL | ncnn YOLOv8 |
| `chuanqi305/MobileNet-SSD/master/{deploy.prototxt,mobilenet_iter_73000.caffemodel}` | 23.3 MB | MIT | Caffe MobileNet-SSD, Pascal-VOC-20 (person, car, bus, motorbike, bicycle, cow, dog…) via `cv2.dnn.readNetFromCaffe` — zero-dependency fallback |
| `opencv/opencv/4.x/data/haarcascades/*.xml` | 0.2–0.9 MB | Apache-2.0 | Also bundled inside `opencv-python` wheel (`cv2.data.haarcascades`, 17 files) |
| `tesseract-ocr/tessdata_fast/main/{eng,hin,osd}.traineddata`; `tessdata_best/main/eng.traineddata` | 4.1 / 1.1 / 10.6 / 15.4 MB | Apache-2.0 | Tesseract LSTM models (English, Hindi, orientation) |

### 1.1 Potholes / road damage

| Model / weights | Where | Reachable via | License | Reported accuracy | Classes |
|---|---|---|---|---|---|
| **RDD2022 (sekilab RoadDamageDetector)** — dataset, not weights. Official pretrained links in README are 2018/2020 TF frozen graphs on `mycityreport` S3 → now `AccessDenied` [V]. | figshare 21431547 | [P] figshare; S3 dead | CC BY-SA 4.0 [V README] | CRDDC'22 winner F1 0.76 overall (YOLO+Faster-RCNN ensemble); India board ≈ 0.42–0.52 for top teams [U] | D00 longitudinal crack, D10 transverse crack, D20 alligator crack, D40 pothole |
| **YOLOv8 RDD models** (`oracl4/RoadDamageDetection` → `YOLOv8_Small_RDD.pt` on HF; `keremberke/yolov8*-pothole-segmentation` on HF) | huggingface.co | **blocked** | AGPL-3.0 | keremberke pothole-seg mAP50 ≈ 0.9 on its own Roboflow split [U] | pothole |
| GitHub-committed `best.pt` pothole/RDD weights (≈ 25 repos checked) | github | **all LFS pointers** [V] | – | – | – |
| **Pothole-600** (Fan et al., RGB-D stereo, 600 images with disparity) | Google Drive | [P] | research | segmentation F1 ~0.8–0.9 in paper [U] | pothole mask |
| **Indian pothole sets**: Kaggle `atulyakumar98/pothole-detection-dataset`, `sachinpatel21/pothole-image-dataset`, `mitangshu11/indian-roads-dataset` (pothole/speed-breaker/unpaved), IIT-style "Indian Roads" sets; **BharatPotHole** (NISER iWatchRoad, 7 000+ dashcam frames, model + dataset announced) | kaggle / smlab.niser.ac.in | [P] both | varies (Kaggle mostly CC0/CC BY; BharatPotHole paper CC BY-NC-SA) | iWatchRoad reports YOLO fine-tune; numbers not extracted [U] | pothole |
| **CMIRD** (Custom Multitask Indian Road Dataset — pothole/crack/waterlogging); student YOLOv8n baseline `yashshree7054/road-hazard-yolov8` | github (weights LFS) | README only | AGPL-3.0 | **honest** held-out numbers: mAP50 0.18, pothole 0.14, crack 0.04 — illustrates how hard in-the-wild Indian frames are [V README] | pothole, crack, waterlogging |

**Practical conclusion:** there is no pip/raw-reachable pretrained pothole model. Plan A: mirror `YOLOv8_Small_RDD.pt` (or train YOLO11n on RDD2022-India + a Kaggle Indian pothole set) once via Tier B and commit it to your own GitHub weights repo (§6.3). Plan B until then: Claude vision on IPM-cropped road patches (Tier C), plus a cheap classical pre-filter (dark blob + texture anomaly on the drivable-area mask from YOLOP).

### 1.2 Traffic signs (Indian)

| Resource | Host / reach | License | Content | Accuracy |
|---|---|---|---|---|
| **Boggartfly/Indian-Expressway-Traffic-Sign-Dataset** [V] | raw.githubusercontent.com (per-file; ~111 MB repo; YOLOv8 layout `train/ validation/ test/` + `data.yaml`) | **MIT** | 21 classes (Ahead only, Bump, Speed 30/50/80/100, Truck Speed 80, Left/Right Curve, No Passing, No Stopping, No U Turn, No Waiting, Steep descent, Work in Progress, Tunnel, …), Mumbai–Pune Expressway dashcam | – |
| **AbhayVAshokan/Traffic-Sign-Detection-Dataset** | raw (labels verified; image path not found — enumerate tree via api.github.com or `git clone`) ; 3.9 GB | none stated | single-class "traffic sign" boxes extracted from IDD, YOLO txt | – |
| **IRTSD-Datasetv1** (IEEE DataPort, DOI 10.21227/ap4b-c439) | [P] needs login | IEEE DataPort terms | 5 141 images, 37 Indian sign classes, 90+ cities | authors: mAP up to 98 % (YOLOv8/10, RT-DETR, in-distribution) [U] |
| **ITSD / IIIT-H Indian Traffic Sign** (Mendeley "Indian Traffic Sign Dataset") ; DataCluster Labs sample on HF | [P] | Mendeley CC BY 4.0 / DataCluster restricted | classification crops (ITSD ~ 85 classes) | – |
| **GTSRB / GTSDB** | benchmark.ini.rub.de, sid.erda.dk [P] | CC0 | German; 43 classes / 900 det images | GTSDB Faster R-CNN Inception-ResNetV2 mAP 95.8 % [U]; nearly saturated |
| **Mapillary Traffic Sign Dataset (MTSD)** | mapillary.com (registration) [P] | CC BY-NC-SA (research) | 52 453 images, 313 classes worldwide incl. India (~5 %) | Faster R-CNN-FPN baseline in paper; substantially harder than GTSDB [U] |
| **CeyRo** (Sri Lanka signs + lights; closest to Indian plates: IRC signs share the Vienna-convention-style shapes) | Google Drive via `oshadajay/CeyRo` README [P] | research | 7 984 images, 70 sign classes + lights | – |
| Indian YOLO sign weights on GitHub (`DMS-ADAS/traffic_sign_detector.pt`, `OpenDrive signDetection.pt`, …) | LFS pointers [V] | – | – | – |

**Recommendation:** detect signs with a generic "sign plate" detector (YOLOP/COCO has no sign class except `stop sign`; train a 1-class plate detector on Boggartfly + AbhayVAshokan + MTSD-India once mirrored), then classify crops with Claude vision against an IRC:67 catalogue (shape/colour/pictogram + OCR). IRC:67 plate sizes (nominal: circular regulatory 600 mm urban / 900 mm NH; triangular cautionary 900 mm side; STOP octagon 900 mm — verify against your IRC:67-2022 copy) double as metric scale references (§4.1).

### 1.3 Zebra crossings, lane markings, arrows, stop lines

| Model | Weights location | Reach | License | Accuracy / notes |
|---|---|---|---|---|
| **YOLOP** (lane line seg + drivable area + vehicles, BDD100K) | **in repo** `weights/End-to-end.pth`, `yolop-{320,640,1280}-{…}.onnx` [V] | **raw ✔** | MIT | BDD100K: lane-line pixel acc 70.5 %, IoU 26.2; drivable mIoU 91.5 % [U, paper]. Lane mask is 2-class (lane-line vs not), so you get *where* the paint is, not its type. |
| **YOLOPv2** | GitHub release `CAIC-AD/YOLOPv2/releases/download/V0.0.1/yolopv2.pt` (156 MB) | release → Tier B (sha in §6) | MIT | better lane IoU (27.2) and drivable mIoU (93.2) [U] |
| **HybridNets** | release `datvuthanh/HybridNets/releases/download/v1.0/hybridnets.pth` (54.7 MB) | Tier B | MIT | lane IoU 31.6, drivable 90.5 [U] |
| **UFLDv2** (Ultra-Fast-Lane-Detection-v2) | Google Drive / Baidu (README) | [P] | MIT | CULane F1 ≈ 75–76 [U]; row-anchor lane *instances* (gives left/right lane lines → width) |
| **CLRNet** | README has no direct link (Google Drive/GitHub release) | – | Apache-2.0 | CULane F1 79.6 (R18) – 80.5 (DLA34) [U]; best accuracy but mmcv-style install |
| **CDNet** (crosswalk detection, YOLOv5-based) | repo zip only; weights via Baidu/Drive | [P] | non-commercial (contact author) | F1 94.8 % average over hard scenarios, >98 % sunny/cloudy, 33 FPS Jetson Nano [U] |
| `xN1ckuz/Crosswalks-Detection-using-YOLO` (YOLOv8, adds stop-line negatives) | no weights in repo | – | GPL-3.0 | code/dataset recipe only |
| GitHub crosswalk/zebra `.pt` (4 repos) | LFS pointers [V] | – | – | – |
| **Mapillary Vistas v2** classes relevant here: `Crosswalk - Plain`, `Lane Marking - Crosswalk`, `Lane Marking - General`, `Lane Marking (only) - Crosswalk`, `Bike Lane`, `Curb`, `Curb Cut`, `Guard Rail`, `Barrier`, `Pole`, `Street Light`, `Traffic Sign (Front/Back)`, `Traffic Light`, `Manhole`, `Catch Basin`, `Sidewalk` (124 classes in v2; `Street Light`/`Manhole` confirmed in v1.2 list, v2 keeps them) [U] | dataset gated; pretrained Vistas models on HF/OpenMMLab | **blocked** | CC BY-NC-SA / commercial licence | – |
| **CeyMo** road-marking dataset (Sri Lanka; 11 classes: straight arrow, left/right arrow, straight-left/right, pedestrian crossing, junction box, slow, bus lane, cycle lane, diamond) | Google Drive [P] | research | 2 887 images; polygon+bbox+mask |

**Classical fallback that works today (Tier A):** warp YOLOP's drivable-area mask region to a bird's-eye view (IPM, §4.1); zebra = periodic high-contrast stripes perpendicular to travel (1-D FFT / autocorrelation along the travel axis over the IPM strip, period ≈ 1.0 m = 0.5 m stripe + 0.5 m gap per IRC:35); stop line = long transverse bright segment (probabilistic Hough on IPM) ahead of the zebra; arrows = connected bright blobs inside the lane with aspect/solidity tests, then classify the crop with Claude. Lane-marking *presence/condition* = contrast ratio of YOLOP lane pixels vs. adjacent asphalt.

### 1.4 Traffic lights

| Resource | Reach | Notes |
|---|---|---|
| COCO class `traffic light` via YOLOv8n/YOLO11n ONNX/ncnn [V] | **raw ✔** | Good for presence; state (red/amber/green) by HSV on the box crop; Claude vision for ambiguous cases. |
| LISA Traffic Light (Kaggle `mbornoe/lisa-traffic-light-dataset`) | [P] | 43 007 frames, US; CC BY-NC-SA |
| Bosch Small Traffic Lights | hci.iwr.uni-heidelberg.de registration [P] | 13 427 images; research licence |
| BDD100K `traffic light` with colour attribute | bdd-data.berkeley.edu / dl.cv.ethz.ch [P] | BSD-style licence; 100 k frames |
| CeyRo (lights included) | Drive [P] | |

### 1.5 Speed breakers / humps / rumble strips

No pretrained model is reachable; the public sets are small: Mendeley "Marked Speed Bump/Speed Breaker Dataset (India)" (969 crops, 2024) [P]; Roboflow `speedbumps-detection` (CC BY 4.0), `speed-breaker` (2 660 images) [P]; Kaggle `mitangshu11/indian-roads-dataset` (speed breaker class) [P]; DriveIndia (TiHAN IIT-H, 66 986 images, 24 classes, YOLO format, "to be released") [U]. Unmarked humps are visually weak; the most reliable signal is **sensor fusion**: a short-duration vertical-acceleration spike (|a_z| > ~0.3 g for 0.2–0.5 s) coincident with a GPS speed dip, and — for marked humps — the IRC:99 alternating black/white or yellow chevron texture in the IPM strip. Treat vision alone as a presence hint and let Claude confirm on the frame.

### 1.6 Road users & encroachments

| Need | Tier-A source | Caveats |
|---|---|---|
| pedestrian, bicycle, motorcycle (two-wheeler), car, bus, truck, cow, dog, horse, sheep, stop sign, traffic light, bench, potted plant, umbrella (hawker proxy) | COCO-80 via YOLOv8n/YOLO11n ONNX/ncnn [V]; MobileNet-SSD VOC [V] as fallback | **No auto-rickshaw class** — COCO calls it car/motorcycle/truck. Encroachment = persistent static objects (carts, umbrellas, benches, parked vehicles) inside the footpath/shoulder band of the IPM; hawkers = person + umbrella/cart cluster off-carriageway. |
| autorickshaw, rider, animal, vehicle-fallback, pole, traffic sign/light, billboard, ego-vehicle | **IDD** (India Driving Dataset; detection 13–15 classes; segmentation 41 classes incl. `animal`, `autorickshaw`, `rider`, `curb`, `guard rail`, `billboard`, `obs-str-bar-fallback`) | idd.insaan.iiit.ac.in registration + academic use; IDD-117K blog on mobility.iiit.ac.in [P]. Mirror via Tier B, fine-tune YOLO11n for `autorickshaw`, `animal`, `rider`, `hawker-cart`. |
| Open Images (has `Auto rickshaw`? no — closest `Taxi`, `Cart`, `Cattle`) | storage.googleapis.com (test) | useful for cart/cattle/umbrella |

### 1.7 Footpaths, kerbs, medians, guardrails, streetlights, poles, drains, manholes (semantic segmentation)

| Model | Weights host | Reach | Licence | Cityscapes / Vistas mIoU [U] | CPU cost |
|---|---|---|---|---|---|
| SegFormer-B0…B5 (Cityscapes/Vistas) | HF `nvidia/segformer-*`, OpenMMLab | blocked | NVIDIA Source Code Licence (research) / mmseg Apache | B0 76.2, B2 81.0 (CS) | B0 ≈ 1–2 s/frame at 1024² CPU |
| Mask2Former / OneFormer (Vistas, Cityscapes panoptic) | HF / fbaipublicfiles | blocked | CC BY-NC (Mask2Former), MIT (OneFormer) | panoptic PQ 66+ (CS) | too heavy for CPU dev |
| DeepLabV3+ (torchvision has only VOC/COCO-stuff) | download.pytorch.org | blocked | BSD | – | – |
| **YOLOv8n-seg / YOLO11n-seg** (COCO instance) [V] | raw ✔ | AGPL | not road furniture | 48 ms |
| MediaPipe `deeplab_v3.tflite` (VOC-21) | storage.googleapis.com (test) | ? | Apache-2.0 | not road furniture | |
| `timm` encoders → HF hub; `segmentation_models_pytorch` encoders → download.pytorch.org + HF (grep of wheel: 8 × pytorch.org, 1 × huggingface) [V-pip] | blocked | – | – | – |
| **YOLOP drivable area** [V] | raw ✔ | MIT | 91.5 mIoU | the only Tier-A "road vs not-road" mask |

Reality: proper footpath/kerb/median/guardrail/streetlight/manhole segmentation needs a Vistas- or IDD-trained model mirrored via Tier B (SegFormer-B1/B2 Vistas is the best CPU-feasible choice; export to ONNX once on a machine that can reach HF). Until then: footpath/kerb presence and continuity from Claude vision on the IPM-ish left/right bands; poles/streetlights by a thin-vertical-blob heuristic on YOLOP's non-road mask plus Claude confirmation; manholes/drains = dark circular/rectangular blobs inside the drivable mask with zebra-like contrast rejection.

### 1.8 OCR for sign text / boards

| Package | Bundled models? | Verified | Notes |
|---|---|---|---|
| **`rapidocr`** 3.10.0 (27 MB wheel) | **Yes**: `rapidocr/models/PP-OCRv6_det_small.onnx` (9.9 MB), `PP-OCRv6_rec_small.onnx` (21.2 MB), `ch_ppocr_mobile_v2.0_cls_mobile.onnx` | [V-pip] | Apache-2.0; CPU-friendly; Chinese+English rec by default; other language recs are downloaded (blocked) — for Hindi/regional scripts use tesseract. |
| **`rapidocr-onnxruntime`** 1.2.3 (12 MB) | Yes: PP-OCRv3 det/rec/cls ONNX | [V-pip] | older line, same licence. |
| `paddleocr` 3.7.0 | No — downloads from `paddle-model-ecology.bj.bcebos.com` | [V-pip grep] | blocked. |
| `easyocr` 1.7.2 | No — every URL in `easyocr/config.py` is `github.com/JaidedAI/EasyOCR/releases/download/…` (craft_mlt_25k.zip, english_g2.zip, devanagari.zip…) | [V-pip grep] | Tier B (sha in §6). Devanagari recogniser is valuable for Hindi boards. |
| **tesseract** (`apt install tesseract-ocr`) + `pytesseract`; traineddata from raw GitHub (`tessdata_fast/eng,hin,osd`, `tessdata_best`) | — | [V] | Apache-2.0; add `tessdata_fast/{mar,tam,tel,kan,ben,guj,pan}.traineddata` per state. |
| `python-doctr` | downloads from mindee CDN | not probed | |

### 1.9 Monocular depth / metric scale

| Model | Host | Reach | Licence | Notes |
|---|---|---|---|---|
| **Depth Anything V2** small/base/large (relative); metric fine-tunes (`*-metric-vkitti-*` outdoor) | HF (`depth-anything/*`) | blocked | **Small: Apache-2.0; Base/Large: CC BY-NC-4.0** | ONNX export `fabio-sim/Depth-Anything-ONNX` release v2.0.0 `depth_anything_v2_vits.onnx` 99.4 MB [V, sha §6]; input 518×518; ~1 s/frame CPU [U]. Relative depth only → needs scale anchor. |
| ZoeDepth (NK) | HF / torch.hub (github release) | blocked | MIT | degrades outdoors vs DA-V2 [U] |
| Metric3D v2, UniDepth v2 | HF | blocked | BSD-2 / CC BY-NC | need intrinsics; best metric zero-shot; heavy |
| MiDaS v2.1 small (`model-small.onnx` 66.8 MB), v3.1 `dpt_swin2_tiny_256.pt` | GitHub releases | Tier B [V sha] | MIT | fast, relative |
| Depth Pro (Apple) | HF | blocked | Apple sample-code licence | metric, focal-length estimation built in; GPU only in practice |
| GitHub-committed `depth_anything_v2_vits.onnx` (10 repos) | — | LFS pointers [V] | – | – |

**What to actually do:** metric widths of ground-plane things (lanes, zebra, shoulders, potholes) do **not** need a depth network — use the flat-road IPM in §4.1, scaled by one of: measured camera height, standard lane width, zebra stripe pitch (IRC:35 500 mm), or sign-plate size (IRC:67). Use a depth network only for *off-ground* geometry (sign mounting height, clearance, median height) and even then anchor its scale to the IPM ground plane in the same frame.

### 1.10 Vision-language model (Claude) as audit reasoner

The product can call the Claude API (`api.anthropic.com` — confirm it is on the allow-list). Use it for *judgement* items a detector can't score: "is the footpath usable/continuous", "is the sign legible/occluded/faded", "is the hump marked and signed in advance", "is there a hazardous kerb drop/open drain", "visibility at this junction". Concrete guidance:

**Model & API (from the `claude-api` skill, Nov-2026):** default `claude-opus-5-5` (adaptive thinking is always on; control depth with `output_config={"effort": "low|medium|high"}` — `low/medium` is right for per-frame checklist scoring); `claude-haiku-5-5` for bulk triage; `claude-sonnet-5-5` is the mid-tier; Message Batches API gives 50 % off for offline runs. No `temperature` on current models; no assistant prefill. Structured output via `client.messages.parse(..., output_format=PydanticModel)` → `response.parsed_output`, or `output_config={"format": {...json schema...}}` on `messages.create`. Images: base64 or Files API; keep ≤ 1 568 px on the long side (≈ 1 600 tokens per 1.15 MP image); include multiple images in one user turn for before/after or left/right context.

**Prompting pattern that works for RSA checklists**
1. **System prompt = the rubric, cached.** Put the IRC-derived definitions (IRC:35 markings, IRC:67 signs, IRC:99 humps, IRC:103 pedestrian facilities, IRC:SP:88 RSA checklist items) and the severity scale in `system` with `cache_control` so it is paid once.
2. **One checklist *group* per call** (e.g., "pedestrian facilities" or "signage"), 6–12 items, not the whole audit; smaller groups reduce omission.
3. **Give the model the facts it cannot see**: chainage, GPS, speed, road class, design speed, time of day, camera type/height, and the detector outputs (boxes with classes/confidences, lane width estimate, IPM-derived distances) as a compact JSON block. Ask it to *verify* detector findings rather than re-detect — Claude's own box coordinates are approximate and should not be used for measurement.
4. **Force ternary answers**: every item is `present | absent | not_visible | not_applicable` plus `confidence (0–1)` and `evidence` (a short literal description of what in the image supports it). "not_visible" prevents hallucinated compliance.
5. **Anti-leading wording**: "Report what is visible; do not infer standards compliance from absence of evidence", and provide 1–2 few-shot examples (one compliant, one deficient) as prior turns.
6. **Structured output** with enums (schema below) and `strict`-style additionalProperties=false; validate server-side and route low-confidence or `not_visible` items to a human reviewer.
7. **Temporal aggregation outside the model**: send key frames every ~10–20 m (or per detector event) and aggregate per 50 m segment in code (majority/any-deficiency), rather than asking the model about a video.
8. **Evaluate** on a human-labelled frame set (≥ 300 frames, 2 auditors) and report per-item agreement (Cohen's κ) before trusting a tier.

```python
from pydantic import BaseModel
from typing import Literal, List
class Item(BaseModel):
    item_id: str                       # e.g. "PED-03 zebra crossing present at junction"
    status: Literal["present","absent","not_visible","not_applicable"]
    condition: Literal["good","faded","damaged","obstructed","unknown"]
    severity: Literal["none","low","medium","high"]
    confidence: float
    evidence: str
class FrameAssessment(BaseModel):
    frame_id: str
    items: List[Item]
    free_text_hazards: List[str]
resp = client.messages.parse(model="claude-opus-5-5", max_tokens=4000,
        output_config={"effort": "medium"}, system=[{"type":"text","text":RUBRIC,"cache_control":{"type":"ephemeral"}}],
        messages=[{"role":"user","content":[{"type":"image","source":{"type":"base64","media_type":"image/jpeg","data":b64}},
                                            {"type":"text","text":context_json + "\nAssess checklist group PED-*."}]}],
        output_format=FrameAssessment)
assessment = resp.parsed_output
```

---

## 2. Datasets (direct URLs and host status)

| Dataset | URL | Host status (sandbox) | Licence | Size / content |
|---|---|---|---|---|
| **RDD2022** full + country zips (India 502 MB) | figshare: `https://figshare.com/articles/dataset/RDD2022_-_The_multi-national_Road_Damage_Dataset_released_through_CRDDC_2022/21431547`; S3 links in sekilab README (`…/Country_Specific_Data_CRDDC2022/RDD2022_India.zip`) now **AccessDenied** [V] | figshare [P] | CC BY-SA 4.0 | 47 420 images, 6 countries; India 9 665 (train 7 706) [U] |
| RDD2020 (India/Japan/Czech) | `https://data.mendeley.com/datasets/5ty2wb6gvg/1`; S3 train.tar.gz dead [V] | [P] | CC BY-SA 4.0 | 26 336 images |
| **IDD** (segmentation 10k/20k, detection, IDD-117K, IDD-3D) | `https://idd.insaan.iiit.ac.in/` (register) ; `https://mobility.iiit.ac.in/idd95k_blog.php` | [P] | research, registration | 41 seg classes incl. autorickshaw, animal, rider, curb, guard rail, billboard |
| Mapillary Vistas v2 | `https://www.mapillary.com/dataset/vistas` (register) | [P] | CC BY-NC-SA; commercial licence available | 25 k images, 124 classes |
| BDD100K | `https://bdd-data.berkeley.edu/` ; mirror `https://dl.cv.ethz.ch/bdd100k/data/` | [P] | BSD-3-style | 100 k frames; det/lane/drivable/seg |
| Cityscapes | `https://www.cityscapes-dataset.com/` (register) | [P] | research | 5 k fine |
| KITTI | `https://www.cvlibs.net/datasets/kitti/` | [P] | CC BY-NC-SA | depth/odometry/det |
| GTSDB / GTSRB | `https://sid.erda.dk/public/archives/ff17dc924eba88d5d01a807357d6614c/FullIJCNN2013.zip`; `https://benchmark.ini.rub.de/` | [P] | CC0 | 900 / 50 k |
| MTSD | mapillary.com/dataset/trafficsign (register) | [P] | CC BY-NC-SA | 52 k |
| CeyRo (signs+lights) / CeyMo (markings) | Drive links in `github.com/oshadajay/CeyRo`, `…/CeyMo` READMEs | [P] | research | 7 984 / 2 887 |
| LISA traffic light | Kaggle `mbornoe/lisa-traffic-light-dataset` | [P] (needs API key) | CC BY-NC-SA | 43 k frames |
| Bosch Small TL | `https://hci.iwr.uni-heidelberg.de/node/6132` | [P] | research | 13 k |
| Indian pothole (Kaggle) | `atulyakumar98/pothole-detection-dataset`, `sachinpatel21/pothole-image-dataset`, `mitangshu11/indian-roads-dataset` | [P] (API key) | mostly CC0/CC BY | 0.6–3 k images each |
| IRTSD-Datasetv1 (Indian signs, 37 cls) | `https://ieee-dataport.org/documents/...` DOI 10.21227/ap4b-c439 | [P] (login) | IEEE DataPort | 5 141 |
| **Boggartfly Indian Expressway Traffic Sign Dataset** | `https://raw.githubusercontent.com/Boggartfly/Indian-Expressway-Traffic-Sign-Dataset/main/{data.yaml,train/*.jpg,*.txt}` | **raw ✔ [V]** (enumerate via api.github.com tree or `git clone`) | MIT | ~111 MB, 21 classes, YOLOv8 layout |
| AbhayVAshokan Traffic-Sign-Detection-Dataset (from IDD) | `https://raw.githubusercontent.com/AbhayVAshokan/Traffic-Sign-Detection-Dataset/master/labels/highquality_16k/...txt` (labels verified; locate images in tree) | raw ✔ for labels [V] | unstated | 3.9 GB repo |
| CDNet crosswalk dataset (6 868 images) | `github.com/zhangzhengde0225/CDNet` → Baidu/Drive | [P] | non-commercial | |
| BharatPotHole / iWatchRoad | `https://smlab.niser.ac.in/project/iwatchroad` | [P] | CC BY-NC-SA (paper) | 7 000+ frames |
| DriveIndia (TiHAN IIT-H) | TiHAN repository (announced, ITSC 2025) | [U] | TBA | 66 986 images, 24 classes YOLO |
| Small Indian dashcam test videos on GitHub | none found with a real committed MP4 (e.g. `cksajil/dash-cam-segmenter/video/demo_video.mp4` → 404) | – | – | Record your own 2–3 min clips (phone + GoPro) and commit them to your weights/fixtures repo. |

---

## 3. Video / sensor ingest

### 3.1 Where the GPS lives

| Source | Metadata | Rate | Extraction |
|---|---|---|---|
| **iPhone (Camera app)** | QuickTime `moov/meta` key `com.apple.quicktime.location.ISO6709` = `+12.9716+077.5946+920.000/` (**one point**, at recording start) plus `…location.accuracy.horizontal` | single | `ffprobe -show_format` or `exiftool -ee -G3 file.MOV`; `hachoir`/`pymediainfo` also read it. No track — pair with a GPX logger app (e.g. "GPS Logger", "Open GPX Tracker") and time-align. |
| **Android (stock camera, "location tags" ON — off by default on many OEMs)** | MP4 `moov/udta/©xyz` ISO 6709 string (`MediaRecorder.setLocation`; Media3 `Mp4LocationData`) | single | `exiftool -ee`, `mp4extract`; **browser uploads strip it** (Addpipe tests) — ingest original files via app/SDK or share-sheet, not `<input type=file>` in a browser. Track: Open Camera (geotag option + separate GPX via app), "GPS Logger for Android", "GPX Logger". |
| **GoPro HERO5–11/13** (HERO12 has **no GPS**) | GPMF `gpmd` data track: `GPS5` (lat, lon, alt WGS84, 2D speed, 3D speed) at 18 Hz (HERO5–9) / 10 Hz (HERO10+), `GPS9` (adds per-sample fix, DOP, time) on HERO11+; also `ACCL`/`GYRO` 200 Hz | 10–18 Hz | PyPI: **`pygpmf-oz`** (0.3.2, GPX export), **`telemetrik`** (pure-python; "filter fix ≥ 3 and DOP < 500"), `gopro-overlay` (0.134), `gopro2gpx`; `exiftool -ee -G3 -api LargeFileSupport=1 -p gpx.fmt`. Accuracy: consumer GNSS ≈ 1–5 m CEP; first 30–60 s often drift until fix. |
| **DJI Osmo Action 4/5** | GPS only via paired phone / DJI GPS Bluetooth remote; written as an **SRT subtitle stream** when "video subtitles" is enabled (`[latitude: …] [longitude: …] [altitude: …]` per frame; same scheme as DJI drones) [U — verify on device] | per frame (~30 Hz nominal, GNSS 1–10 Hz) | `ffmpeg -i in.MP4 -map 0:s:0 out.srt` then regex; `pysrt`. |
| **Insta360 (X3/X4/Ace Pro)** | GPS in `.insv` metadata when paired with phone/GPS remote; readable with `exiftool -ee` (per-sample `GPSLatitude…`) ; Gyroflow's `telemetry-parser` also reads Insta360/GoPro/DJI [U] | ~1–10 Hz | exiftool → GPX |
| **Ray-Ban Meta glasses** | **no GPS in video**; POV 1080p/30, ~1-3 min clips; location only via phone app | – | Run a GPX logger on the phone; align by UTC (`creation_time` in MOV) + manual offset check. |
| Action-cam / phone common | `creation_time` is often local time without offset — always resolve with a visible clock or GPS time from the track. | | |

`exiftool` = `apt install libimage-exiftool-perl`; `PyExifTool` 0.5.6 on PyPI [V-pip]; `gpxpy` 1.6.2 for GPX; `av` 19 / `ffmpeg-python` for frame + subtitle demux.

### 3.2 Camera intrinsics and extrinsics

* **Stills**: EXIF `FocalLength` + `FocalLengthIn35mmFilm` (f35) → `f_px = f35 · W_px / 36` (horizontal; use 24 mm for the vertical if needed). Also `LensModel`, `DigitalZoomRatio`.
* **Video**: no EXIF. Use a device table keyed on `com.apple.quicktime.model` / Android `©mod`/`com.android.version` or the user's selection. Typical main cameras: 24–26 mm-eq → HFOV ≈ 70–74°; `f_px = W / (2 tan(HFOV/2))` → for 1920 px and 26 mm-eq, f ≈ 1 380 px; 4K (3840) ≈ 2 760 px. Ultra-wide 13 mm-eq ≈ 120° (strong distortion — avoid). GoPro: use **Linear** or Linear+Horizon-Lock FOV (≈ 86–92°) and *disable HyperSmooth*; SuperView/Wide are fisheye and need per-mode undistortion. DJI Osmo Action: "Dewarp" on. Glasses (Ray-Ban Meta): ≈ 100° diagonal, mild distortion, no stabilisation control.
* **Calibrate once per device** with a checkerboard (`cv2.calibrateCamera`) or, cheaper, from the road itself: vanishing point of the lane lines gives pitch/yaw, and the known lane width gives height (§4.1). Store `(fx, fy, cx, cy, k1, k2, h, pitch)` per session.
* **Camera height h**: dash-mounted sedan 1.2–1.4 m, SUV/pickup 1.5–1.8 m, bus 2.2–2.6 m; two-wheeler helmet-cam 1.5–1.7 m; handheld/chest 1.3–1.5 m; glasses 1.5–1.7 m (standing/walking). Measure it — height error is a *proportional* width error.
* **Stabilisation pitfalls**: EIS (iPhone default, HyperSmooth, RockSteady) crops 10–20 % and applies time-varying warps so `K` and the horizon move frame-to-frame; rolling-shutter + vibration bends poles/lane lines; Apple "Action mode" and GoPro "Horizon lock" rotate the frame so the camera's roll is no longer the vehicle's. Prefer stabilisation OFF for measurement sessions, re-estimate the horizon per frame (lane vanishing point / IMU), and never trust a single frame for width — use a median over 10–20 frames.

---

## 4. Geometry from monocular video

### 4.1 Inverse Perspective Mapping (flat-road model)

Pinhole camera with intrinsics `K = [[f,0,c_x],[0,f,c_y],[0,0,1]]`, mounted at height `h` above a locally flat road, pitched **down** by `θ` (roll and yaw ≈ 0 after rectifying with the lane vanishing point). World frame: origin under the camera, `X` right, `Y` down, `Z` forward (horizontal). Pixel `(u,v)` → normalised `x = (u − c_x)/f`, `y = (v − c_y)/f`. The ray in world coordinates is

`r(x,y) = ( x ,  y·cosθ + sinθ ,  cosθ − y·sinθ )`

Intersecting with the ground plane `Y = h` gives `λ = h / (y cosθ + sinθ)` and the metric ground point

```
Z(u,v) = h · ( f·cosθ − (v − c_y)·sinθ ) / ( (v − c_y)·cosθ + f·sinθ )
X(u,v) = h · ( u − c_x )                 / ( (v − c_y)·cosθ + f·sinθ )
```

* **Horizon row** `v_h = c_y − f·tanθ` (denominator → 0). Hence **pitch from the vanishing point**: `θ = atan((c_y − v_h)/f)`, with `v_h` from the intersection of the two lane lines (YOLOP lane mask → Hough/RANSAC lines) or from the IMU.
* **Lateral width of anything on the road at image row v**: two points `u_1,u_2` on the same row satisfy `ΔX = h·(u_2 − u_1) / ((v − c_y)cosθ + f sinθ)`. This is how lane width, zebra length, pothole width and shoulder width are read.
* **Scale from a known width** (when `h` is unknown or the camera is handheld): `h = W_known · ((v − c_y)cosθ + f sinθ) / (u_2 − u_1)`. Known widths: standard lane 3.5 m (IRC:73/86; 3.75 m single-lane NH; **only** where you are confident it is standard), zebra stripe pitch 1.0 m (0.5 m stripe + 0.5 m gap, IRC:35), zebra stripe width 0.5 m, sign plates per IRC:67 (600/900 mm circles, 900 mm triangle side, 900 mm STOP) — a vertical plate gives `Z = f·D_real/d_px` from its pixel size, which then calibrates `h` through the plate's foot row.
* **Full IPM image**: pick ground ROI `X∈[−8,8] m, Z∈[3,30] m`, pixel pitch 2 cm, compute the homography `H = K·[r_1 r_2 t]` (rotation about X by θ, translation `(0,h,0)`) and `cv2.warpPerspective` with `WARP_INVERSE_MAP`. Do zebra/stop-line/arrow logic and lane-width measurement on this top view.
* **Error budget** (set expectations): with `Z ≈ h f/(v − c_y)` for small θ, `∂Z/∂v = −Z²/(h f)` → at Z = 10 m, h = 1.3 m, f = 1 400 px, one pixel row = 5.5 cm; at 20 m, 22 cm. Lateral width error ∝ `δh/h` (height) and ≈ `(Z/h)·δθ` fraction from pitch (0.5° pitch error at Z = 10 m ≈ 6 % of Z longitudinally but only ~1 % laterally if the horizon is re-estimated per frame). Non-flat roads (crest, superelevation, humps) violate the model: measure widths at 6–15 m ahead where the road is still "locally flat" and the pixel resolution is good, and take the median over many frames.

**Lane width** = `|X_left(v) − X_right(v)|` of the two YOLOP lane-line clusters (or UFLDv2/CLRNet lane instances) evaluated at rows corresponding to Z = 6–12 m, median over ≥ 15 frames and per 20 m of chainage; report with the `±` from the error budget. Carriageway width = outer edge lines (or asphalt/soil boundary from the drivable-area mask) when no inner markings exist, which is common on Indian rural roads.

### 4.2 Horizontal curvature

**From the GPS track.** Convert to local ENU (`x = R cosφ_0 Δλ, y = R Δφ`, R = 6 371 008 m), resample by distance (2–5 m) after Kalman/Savitzky–Golay smoothing. Over a sliding window of arc length L (50–150 m; longer for gentler curves) fit a circle:

* Kåsa algebraic fit: minimise `Σ (x_i² + y_i² + D x_i + E y_i + F)²` → linear least squares; centre `(−D/2, −E/2)`, `R = √(D²/4 + E²/4 − F)`. Pratt/Taubin fits are less biased for short arcs (`scipy.optimize.least_squares` geometric refinement optional).
* Or heading-rate: `κ = dψ/ds` with `ψ = atan2(dy, dx)` unwrapped; `R = 1/κ`. Classify curve/tangent by `|κ| > 1/1000 m⁻¹` sustained over ≥ 30 m; curve length, deflection angle `Δ = ∫κ ds`, and (with speed) side friction demand `f = v²/(gR) − e`.
* Accuracy: consumer GNSS at 1–10 Hz with σ ≈ 2–5 m gives usable radii for **R ≲ 300–500 m** (≈ ±5–15 %); for R > 1 000 m the noise dominates. Mobile-mapping-grade data achieves ≈ 5 % average radius error (Luo et al. 2018); smartphone + EKF studies (Zhang/Wood 2018) report "reasonable" agreement without hard numbers [U]. Fuse the gyroscope yaw-rate (`κ = ω_z / v`) where the camera/phone provides IMU — it is far less noisy at short wavelengths.

**From the image.** Fit `x(z) = a + b z + c z² (+ d z³)` to each lane line in IPM coordinates; curvature at the vehicle `κ ≈ 2c/(1 + b²)^{3/2}`. Good only for the next 20–40 m and sensitive to pitch; use it to confirm GPS curves and to detect curve **start** precisely for sign-placement checks (advance warning distance per IRC:67 ≈ 45–120 m depending on speed).

### 4.3 Gradient (vertical alignment)

* GPS altitude: vertical σ is 1.5–3× horizontal (5–15 m). Only a **regression over ≥ 200–500 m** gives ±1 % grade; fine for flagging long grades, useless for short crests.
* **Barometer** (most phones, GoPro HERO9+, DJI, Insta360 export pressure in telemetry): `Δh ≈ −(R·T)/(g·M) · ln(p/p_0) ≈ 8.4 m per hPa` at sea level; phone barometers resolve ≈ 0.1 hPa (≈ 1 m) with slow weather drift → grade over 100 m windows to ≈ ±0.5–1 %. Combine: barometer for shape, GPS for long-term level.
* **IMU**: pitch from accelerometer with speed-derived longitudinal acceleration removed (`θ_road ≈ asin((a_x − dv/dt)/g)`); Gupta et al. (IPSN 2020) report 90 % of grade errors < 0.3° (≈ 0.5 %) with gyro+accelerometer fusion [U].
* DEM fallback (SRTM-30 m/Copernicus-30 m) if an allow-listed source exists — too coarse for anything but long grades.

### 4.4 Sight-distance proxies

* **Available Sight Distance (ASD) from the image**: furthest row of the YOLOP drivable-area mask contiguous with the ego lane → `Z` via §4.1 (cap at 2–3× camera-height-limited range, ≈ 60–100 m for phone cameras; beyond that the pixel resolution is too coarse). Compare against IRC:66/IRC:73 SSD for the posted/design speed (e.g., 50 km/h ≈ 60 m, 65 ≈ 90 m, 80 ≈ 120 m, 100 ≈ 180 m — confirm with your IRC copy). Flag segments where ASD < SSD, especially on crests (grade change from §4.3) and inside curves.
* **Geometric horizontal-curve check**: with curve radius R and lateral obstruction setback M (from the drivable mask/kerb/vegetation in IPM), `ASD = 2R·acos(1 − M/R)` (middle-ordinate relation) for ASD ≤ curve length.
* **Vertical crest**: `S = √(2·a·h_1) + √(2·a·h_2)`-type relations need grade difference A from §4.3; treat as coarse.

### 4.5 Visual odometry (optional)

OpenCV-only monocular VO: ORB/SIFT (`cv2.SIFT_create` is in `opencv-python` ≥ 4.4) → `cv2.findEssentialMat(RANSAC)` → `cv2.recoverPose`; scale is unobservable — fix it with GPS speed or the ground-plane height (`h` known → scale from triangulated road points). Useful for (a) frame-to-frame pitch/roll (stabilising IPM), (b) interpolating between 1 Hz GPS fixes, (c) tunnels. ORB-SLAM3 / DROID-SLAM are not pip-installable; `pyslam` is source-only. Don't build the chainage on VO alone — drift is 1–3 % of distance.

---

## 5. Honest accuracy expectations

| Task | Best published (clean benchmark) | Realistic for Indian smartphone/action-cam video | Source |
|---|---|---|---|
| Road damage detection (4-class RDD2022) | F1 0.76 overall (CRDDC'22 winner, YOLO+Faster-RCNN ensemble); **India test board 0.42–0.52** even for top-5 teams (YOLOv7 team: India F1 0.516) | **pothole-only F1 0.6–0.75** after fine-tuning on Indian data and frame-level aggregation; cracks 0.3–0.5 | arXiv 2211.11362; 2211.00091; Geoscience Data J. 2024 |
| Pothole (single-class curated sets) | mAP50 0.85–0.95 in-distribution | drops to 0.3–0.6 cross-domain (CMIRD student baseline: pothole mAP50 0.14 on held-out video split) | keremberke/Roboflow cards [U]; CMIRD README [V] |
| Pothole size | area error ≈ 9.7 % (UAV, IPM + YOLOv8); depth 4 % on one sample | width ±20–30 % from a dashcam; depth not measurable monocularly without stereo/structured light | ResearchGate 2025 [U] |
| Traffic sign detection | GTSDB mAP 95.8 % (saturated); MTSD and Indian IRTSD claim ~98 % in-distribution | presence/recall 0.85–0.95 for common regulatory/warning plates; classification of ~60 IRC classes 0.8–0.9 with VLM assist; faded/vandalised/non-standard boards are the long tail | Mishra ACCV-W 2022; IRTSD DataPort [U] |
| Crosswalk detection | CDNet F1 94.8 % (hard scenes), > 98 % sunny | 0.85–0.9 presence; faded zebra (very common) is the main miss — condition grading needs the IPM contrast metric | NCAA 2022 [U] |
| Lane line detection | CLRNet CULane F1 80.5; UFLDv2 ≈ 76; YOLOP lane IoU 26 / acc 70 % | unmarked/eroded rural lanes → fall back to asphalt-edge width | papers [U] |
| Lane / carriageway width | no dashcam-vs-survey RMSE paper found; LiDAR-camera mapping σ 0.22 m | **±0.10–0.30 m** at 6–15 m with calibrated h/θ and per-frame horizon; ±0.5 m uncalibrated handheld | §4.1 error budget; arXiv 2405.07544 |
| Horizontal radius | MMS 4.9 % average error | ±5–15 % for R < 300 m from phone GPS @1 Hz; unreliable above ~1 km | Luo 2018; Wood & Zhang 2018 [U] |
| Grade | gyro+accel fusion 90 % < 0.3° | ±0.5–1 % over 100 m with barometer; ±1 % over 300 m GPS-only | Gupta IPSN 2020 |
| Metric depth (off-ground) | DA-V2 metric outdoor AbsRel ≈ 0.05–0.10 on KITTI-like; MAE 0.45 m short-range field test | ±10–20 % after IPM anchoring; heights of signs/medians ±0.2–0.4 m | Depth Pro / camera-trap studies [U] |
| Semantic segmentation (sidewalk/curb/pole…) | SegFormer-B2 Cityscapes 81 mIoU; Vistas ~ 50 mIoU (124 cls) | small classes (manhole, catch basin, street light) 30–50 IoU; use for presence per segment, not pixel-accurate | papers [U] |

**Against the "98 %" target:** 98 % is attainable only for *frame-level presence of large, well-lit objects* (vehicles, people, traffic lights, intact zebra) and for *binary segment-level* items after temporal aggregation and human review of flagged uncertainties. For potholes/cracks, faded markings, rural sign condition and any metric quantity, publish precision/recall per item from your own labelled set and design the workflow as "AI pre-audit + auditor confirmation" (IRC:SP:88 still requires a qualified auditor's sign-off anyway).

---

## 6. Recommended stack

### 6.1 Tier A — pip + raw.githubusercontent.com only (works today on the CPU box)

```
pip install onnxruntime ncnn opencv-python-headless numpy scipy shapely pyproj gpxpy \
            rapidocr pytesseract pyexiftool pygpmf-oz telemetrik av ffmpeg-python \
            ultralytics  # training/export utilities; no weights are downloaded unless you ask
apt install tesseract-ocr libimage-exiftool-perl ffmpeg
```

| Capability | Component | Source [V] |
|---|---|---|
| Road users, traffic lights, animals, stop sign, hawker proxies | `yolov8n.onnx` (35 ms) / `yolov8m.onnx` (176 ms) via onnxruntime; or `yolo11n.ncnn.*` via ncnn | Hyuto / AndreyGermanov / nihui URLs in §6.2 |
| Instance masks (vehicles, people) | `yolov8n-seg.onnx`, `yolo11n_seg.ncnn.*` | same |
| Drivable area, lane-line pixels, vehicles | `yolop-640-640.onnx` (247 ms; batch frames every 0.5 s) | hustvl/YOLOP (MIT) |
| Sign/board text, speed-limit numerals | RapidOCR (bundled PP-OCRv6) + tesseract eng/hin | PyPI; tessdata raw |
| Zebra/stop-line/arrow/hump-marking geometry, lane width, IPM | OpenCV on YOLOP masks (§1.3, §4.1) | – |
| GPS/IMU ingest, chainage, curvature, grade | exiftool/pygpmf/telemetrik + gpxpy + scipy | PyPI |
| Legacy fallback detector | MobileNet-SSD Caffe via `cv2.dnn` | chuanqi305 |
| (test first) COCO detector w/o AGPL | MediaPipe EfficientDet-Lite0/2 TFLite from `storage.googleapis.com` (sha256 in §6.2) with `ai-edge-litert`/`mediapipe` | Google (Apache-2.0) |

Licence note: every YOLOv5/8/11 weight is AGPL-3.0; shipping them in a networked product means AGPL-compliance (publish source) or an Ultralytics Enterprise licence. YOLOP (MIT), YOLOX (Apache-2.0, Tier B), NanoDet (Apache-2.0, `nanodet_m` ncnn in Tier A), EfficientDet-Lite (Apache-2.0) and MobileNet-SSD (MIT) are the permissive alternatives — decide before Tier B fine-tuning.

### 6.2 Verified download table (URL · bytes · sha256)

**Reachable now (raw.githubusercontent.com):**

| URL | Bytes | sha256 |
|---|---|---|
| https://raw.githubusercontent.com/hustvl/YOLOP/main/weights/yolop-640-640.onnx | 35 902 568 | `cd66a3e0087a7258ae07768cc02cb742eed93865727ae4c9baf969b8fa190696` |
| https://raw.githubusercontent.com/hustvl/YOLOP/main/weights/End-to-end.pth | 95 756 827 | `620e7495328cfc8e04807c14cbb8f8df9916953359d190cbf494b2d049f03b0c` |
| https://raw.githubusercontent.com/Hyuto/yolov8-onnxruntime-web/master/public/model/yolov8n.onnx | 12 821 996 | `505648ada344cd9f3f31e51d49c489c070819bc96cc758258a8fd51488e00579` |
| https://raw.githubusercontent.com/Hyuto/yolov8-seg-onnxruntime-web/master/public/model/yolov8n-seg.onnx | 13 841 543 | `373a09e8341a74c22b186a4ba2a2c4b3618b7862147976d48f581d251b071873` |
| https://raw.githubusercontent.com/AndreyGermanov/yolov8_onnx_python/main/yolov8m.onnx | 103 773 493 | `e91bd39ce15420f9623d5e3d46580f7ce4dfc85d061e4ee2e7b78ccd3e5b9453` |
| https://raw.githubusercontent.com/nihui/ncnn-assets/master/models/yolov8n.ncnn.bin (+ `.param`, 15 250 B) | 6 315 484 | `c7c01d61a7b9b9fe5c5e5300dcc6413777de93083fe4765a2af190d94bc15dcf` |
| https://raw.githubusercontent.com/nihui/ncnn-assets/master/models/yolo11n.ncnn.bin (+ `.param`) | 5 249 340 | `2e1b06fa4210739a71d0bf3132e2f6560e46281e8e071292f2857b3bda726285` |
| https://raw.githubusercontent.com/nihui/ncnn-assets/master/models/yolov8n_seg.ncnn.bin | 6 821 392 | `95bf477401249a46dccbd481ca6b46f74f1216a09dd161bd8d725ae291454432` |
| https://raw.githubusercontent.com/nihui/ncnn-assets/master/models/yolo11n_seg.ncnn.bin | 5 755 248 | `454969047fcc4dd0ff45b9da019cce1ba4b155b15eb281a27816e769528b1aef` |
| https://raw.githubusercontent.com/nihui/ncnn-assets/master/models/yolov8s_worldv2.ncnn.bin | 25 770 232 | `e06f3386373612a4cef5a3a181c654d8c7dd8e9379a411967dfe90a8c9354eac` |
| https://raw.githubusercontent.com/nihui/ncnn-assets/master/models/yolov6n.bin | 8 644 816 | `2b1fe6a3fe845b93303faea70244e4cd138b5781a6971a385cda6580026ebe6f` |
| https://raw.githubusercontent.com/Qengineering/YoloV8-ncnn-Raspberry-Pi-4/main/yolov8n.bin | 6 315 484 | `ae8ea22b22c9fec92c7197f3b293e4badb459ee31a08dacad3331f660dc81cbb` |
| https://raw.githubusercontent.com/chuanqi305/MobileNet-SSD/master/mobilenet_iter_73000.caffemodel (+ `deploy.prototxt`) | 23 306 119 | `52eed8be80522c152a17fb56740de705b79881bde1a167e0e747310523685fc7` |
| https://raw.githubusercontent.com/tesseract-ocr/tessdata_fast/main/eng.traineddata | 4 113 088 | `7d4322bd2a7749724879683fc3912cb542f19906c83bcc1a52132556427170b2` |
| https://raw.githubusercontent.com/tesseract-ocr/tessdata_fast/main/hin.traineddata | 1 122 751 | `4c73ffc59d497c186b19d1e90f5d721d678ea6b2e277b719bee4e2af12271825` |
| https://raw.githubusercontent.com/Boggartfly/Indian-Expressway-Traffic-Sign-Dataset/main/data.yaml (dataset, MIT) | 327 | – |

**Test-from-build-box (storage.googleapis.com):** `https://storage.googleapis.com/mediapipe-models/object_detector/efficientdet_lite0/float32/latest/efficientdet_lite0.tflite` 13 836 895 B `40338edf5ec70d43e318b0a716a84d4564cd1802759a7a07170c7e43796dbf58`; `…/efficientdet_lite2/float32/latest/efficientdet_lite2.tflite` 23 096 891 B `ad2abbf2b4e10585e15176fd7b5ef03c28dda959ae26fc142549fdd1814db91d`.

### 6.3 Tier B — one-time downloads (GitHub releases / HF) to mirror into your own repo

Mirror procedure: on any machine with normal internet, download, verify sha256, then push to a **private GitHub repo `cfi-weights` without Git LFS** (keep each file < 100 MB; `split -b 95M yolopv2.pt yolopv2.pt.part-` and `cat` on the build box). The build machine then fetches `https://raw.githubusercontent.com/<org>/cfi-weights/main/<file>`. Also ask IT to allow-list `objects.githubusercontent.com` + `github.com` and `huggingface.co` (+ `cdn-lfs.huggingface.co`) — that alone removes most of this tier.

| File | URL | Bytes | sha256 [V] | Licence | Use |
|---|---|---|---|---|---|
| yolov8n.pt | https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n.pt | 6 549 796 | `f59b3d833e2ff32e194b5bb8e08d211dc7c5bdf144b90d2c8412c47ccfc83b36` | AGPL-3.0 | fine-tune base |
| yolov8s.pt | …/v8.3.0/yolov8s.pt | 22 588 772 | `1f47a78bf100391c2a140b7ac73a1caae18c32779be7d310658112f7ac9aa78a` | AGPL | |
| yolov8n-seg.pt | …/v8.3.0/yolov8n-seg.pt | 7 071 756 | `a7cd8f929e1903d78a12a48efecab430209f18dc46cb96c3599a5980c63c423c` | AGPL | pothole-seg fine-tune |
| yolo11n.pt | …/v8.3.0/yolo11n.pt | 5 613 764 | `0ebbc80d4a7680d14987a577cd21342b65ecfd94632bd9a8da63ae6417644ee1` | AGPL | preferred fine-tune base |
| yolo11s.pt | …/v8.3.0/yolo11s.pt | 19 313 732 | `85a76fe86dd8afe384648546b56a7a78580c7cb7b404fc595f97969322d502d5` | AGPL | GPU prod |
| yolo11n-seg.pt | …/v8.3.0/yolo11n-seg.pt | 6 182 636 | `55ed65c56c91713d23e8402371c6c49a6fd84f257f7dce452e8d70e41dcbe152` | AGPL | |
| yolopv2.pt | https://github.com/CAIC-AD/YOLOPv2/releases/download/V0.0.1/yolopv2.pt | 156 380 200 | `f2a8c8374203ae3e67ff9c184e931f763957de92a993b23269e4e721627f1f8c` | MIT | better lanes (split for mirror) |
| hybridnets.pth | https://github.com/datvuthanh/HybridNets/releases/download/v1.0/hybridnets.pth | 54 732 155 | `b11271048773051c54a3adbc2586fe2b395f9feb72c641a4fb45ce1761c2678e` | MIT | lanes + drivable |
| MiDaS v2.1 small ONNX | https://github.com/isl-org/MiDaS/releases/download/v2_1/model-small.onnx | 66 764 249 | `2d8c6cb8f415229daf1eb041024208e2608c9f98e17c81cc7c6ecb449c56fd58` | MIT | fast relative depth |
| MiDaS v3.1 dpt_swin2_tiny_256 | https://github.com/isl-org/MiDaS/releases/download/v3_1/dpt_swin2_tiny_256.pt | 172 162 911 | `0a859caa18be4bf9375e87dc6b684f6e83dc45b2dc13d8c8b89f6acb2a17a2c5` | MIT | |
| Depth-Anything-V2 small ONNX | https://github.com/fabio-sim/Depth-Anything-ONNX/releases/download/v2.0.0/depth_anything_v2_vits.onnx (input `1×3×518×518`) | 99 373 606 | `d2b11a11c1d4a12b47608fa65a17ee9a4c605b55ee1730c8e3b526304f2562be` | Apache-2.0 | relative depth |
| EasyOCR CRAFT detector | https://github.com/JaidedAI/EasyOCR/releases/download/pre-v1.1.6/craft_mlt_25k.zip | 77 251 756 | `8dc6a1c703a89ed56308ef742d26ebd45c656248cbbbda6e7fe60e569f873e65` | Apache-2.0 | text detection |
| EasyOCR english_g2 | https://github.com/JaidedAI/EasyOCR/releases/download/v1.3/english_g2.zip | 14 040 947 | `1b5eaebf1c062de6205560c97ffcfa8dc0e6f413c340e8adc5cfc57e159f61ff` | Apache-2.0 | (+ `pre-v1.1.6/devanagari.zip` for Hindi) |
| YOLOX-s | https://github.com/Megvii-BaseDetection/YOLOX/releases/download/0.1.1rc0/yolox_s.pth | 72 089 125 | `f55ded7181e1b0c13285c56e7790b8f0e8f8db590fe4edb37f0b7f345c913a30` | Apache-2.0 | permissive COCO detector / fine-tune base |
| YOLOX-nano | …/0.1.1rc0/yolox_nano.pth | 7 694 953 | `cd28f55fbbc1829f99d9ac9b38a16d259a22889739c8728ea877610201feff7b` | Apache-2.0 | CPU |
| RDD YOLOv8-small | HF `oracl4/RoadDamageDetection` → `YOLOv8_Small_RDD.pt` [U, no sha] | ~22 MB | – | AGPL | immediate pothole/crack baseline |
| keremberke pothole seg | HF `keremberke/yolov8n-pothole-segmentation` [U] | ~7 MB | – | AGPL | |
| SegFormer-B2 Vistas / Cityscapes | HF `nvidia/segformer-b2-finetuned-cityscapes-1024-1024`; Vistas variants via mmseg [U] | ~110 MB | – | NVIDIA research licence | footpath/kerb/pole/guardrail |
| Depth-Anything-V2 metric outdoor (vKITTI, small) | HF `depth-anything/Depth-Anything-V2-Metric-VKITTI-Small-hf` [U] | ~100 MB | – | Apache-2.0 (small) | metric heights |
| Datasets to mirror (same repo or object storage): RDD2022_India (502 MB, figshare), IDD-Detection + IDD-Segmentation (registration), Mapillary Vistas (registration), CeyRo/CeyMo, LISA, Bosch, Kaggle Indian pothole sets, IRTSD. | | | | | |

### 6.4 Verify-before-trust snippet (for any raw.githubusercontent URL)

```bash
# prints size and whether the blob is a Git-LFS pointer
u=$1; curl -sI "$u" | awk 'tolower($1)=="content-length:"{print "bytes:",$2}'; curl -s -r 0-60 "$u" | grep -q 'git-lfs' && echo "LFS POINTER — unusable" || echo "real file"
sha256sum <(curl -sL "$u")
```

### 6.5 Tier C — Claude vision

* Per 50 m segment: 2–4 key frames (forward + the IPM top view) → `claude-haiku-5-5` for triage of all checklist groups; escalate flagged/uncertain items to `claude-opus-5-5` (effort `medium`). Use Message Batches for offline audits; prompt-cache the rubric; `messages.parse` with the schema in §1.10.
* Budget guide (approx.): one 1 600-token image + 1 500-token context ≈ 3 k input tokens; a 10 km audit at 1 frame/25 m ≈ 400 frames ≈ 1.2 M input tokens.
* Keep humans in the loop for anything the model marks `not_visible` or `confidence < 0.6`; log the `evidence` strings into the report as auditor-readable justifications.

### 6.6 CPU-dev → GPU-prod path

Dev (4-core CPU): sample video at 2 fps, 640 px; YOLOv8n-ONNX (35 ms) + YOLOP every 2nd sample (247 ms) + RapidOCR on sign crops → ~1–1.5 fps end-to-end, i.e. 10 km of 30 km/h footage (~20 min) processes in ~30–40 min. Prod (GPU): swap to YOLO11s/YOLOPv2/SegFormer-B2 + Depth-Anything-V2 at 5–10 fps; same ONNX pipeline with `CUDAExecutionProvider`/TensorRT; ultralytics for fine-tuning on mirrored RDD2022-India + IDD + Boggartfly + own labelled frames.

---

## Sources

Models / repos (verified by fetch): [sekilab/RoadDamageDetector README](https://raw.githubusercontent.com/sekilab/RoadDamageDetector/master/README.md) · [hustvl/YOLOP](https://github.com/hustvl/YOLOP) (weights in repo, MIT) · [CAIC-AD/YOLOPv2](https://github.com/CAIC-AD/YOLOPv2) · [datvuthanh/HybridNets](https://github.com/datvuthanh/HybridNets) · [cfzd/Ultra-Fast-Lane-Detection-v2](https://github.com/cfzd/Ultra-Fast-Lane-Detection-v2) · [Turoad/CLRNet](https://github.com/Turoad/CLRNet) · [zhangzhengde0225/CDNet](https://github.com/zhangzhengde0225/CDNet) · [xN1ckuz/Crosswalks-Detection-using-YOLO](https://github.com/xN1ckuz/Crosswalks-Detection-using-YOLO) · [Hyuto/yolov8-onnxruntime-web](https://github.com/Hyuto/yolov8-onnxruntime-web) · [AndreyGermanov/yolov8_onnx_python](https://github.com/AndreyGermanov/yolov8_onnx_python) · [nihui/ncnn-assets](https://github.com/nihui/ncnn-assets) · [Qengineering/YoloV8-ncnn-Raspberry-Pi-4](https://github.com/Qengineering/YoloV8-ncnn-Raspberry-Pi-4) · [chuanqi305/MobileNet-SSD](https://github.com/chuanqi305/MobileNet-SSD) · [tesseract-ocr/tessdata_fast](https://github.com/tesseract-ocr/tessdata_fast) · [isl-org/MiDaS](https://github.com/isl-org/MiDaS) · [fabio-sim/Depth-Anything-ONNX](https://github.com/fabio-sim/Depth-Anything-ONNX) · [Megvii-BaseDetection/YOLOX](https://github.com/Megvii-BaseDetection/YOLOX) · [RangiLyu/nanodet](https://github.com/RangiLyu/nanodet) · [JaidedAI/EasyOCR](https://github.com/JaidedAI/EasyOCR) · [RapidAI/RapidOCR (PyPI `rapidocr`)](https://pypi.org/project/rapidocr/) · [Boggartfly/Indian-Expressway-Traffic-Sign-Dataset](https://github.com/Boggartfly/Indian-Expressway-Traffic-Sign-Dataset) · [AbhayVAshokan/Traffic-Sign-Detection-Dataset](https://github.com/AbhayVAshokan/Traffic-Sign-Detection-Dataset) · [yashshree7054/road-hazard-yolov8 (CMIRD baseline)](https://github.com/yashshree7054/road-hazard-yolov8) · [oshadajay/CeyRo](https://github.com/oshadajay/CeyRo) · [oshadajay/CeyMo](https://github.com/oshadajay/CeyMo) · [Ultralytics licence](https://ultralytics.com/license) · [Roboflow on YOLOv8 licensing](https://roboflow.com/model-licenses/yolov8) · [MediaPipe models bucket](https://storage.googleapis.com/mediapipe-models/)

Benchmarks / papers: [CRDDC'2022 challenge paper, arXiv 2211.11362](https://arxiv.org/abs/2211.11362) · [RDD2022 data paper, arXiv 2209.08538](https://arxiv.org/pdf/2209.08538) · [RDD2022, Geoscience Data Journal 2024](https://rmets.onlinelibrary.wiley.com/doi/10.1002/gdj3.260) · [YOLOv7 for CRDDC, arXiv 2211.00091](https://arxiv.org/html/2211.00091v1) · [CDNet, Neural Computing & Applications 2022](https://zhangzhengde0225.github.io/publication/2020-CDNet) · [Mapillary Traffic Sign Dataset, arXiv 1909.04422](https://arxiv.org/pdf/1909.04422) · [Mishra et al., ACCV-W 2022 traffic-sign benchmarking](https://openaccess.thecvf.com/content/ACCV2022W/DLSOD/papers/Mishra_Evaluating_and_Bench-marking_Object_Detection_Models_for_Traffic_Sign_and_ACCVW_2022_paper.pdf) · [GTSDB SOTA table](https://vercel.hyper.ai/en/sota/tasks/traffic-sign-detection/benchmark/traffic-sign-detection-on-gtsdb) · [Mapillary Vistas (Neuhold et al., ICCV 2017)](https://openaccess.thecvf.com/content_ICCV_2017/papers/Neuhold_The_Mapillary_Vistas_ICCV_2017_paper.pdf) · [Vistas 2.0 announcement](https://blog.mapillary.com/update/2021/01/18/vistas-2-dataset.html) · [IDD-117K detection](https://mobility.iiit.ac.in/idd95k_blog.php) · [IDD (WACV 2019)](https://cseweb.ucsd.edu/%7Emkchandraker/pdf/wacv19_idd.pdf) · [IRTSD / Indian sign datasets on IEEE DataPort](https://ieee-dataport.org/node/13266) · [Marked Speed Bump dataset (India), Mendeley](https://data.mendeley.com/datasets/bvpt9xdjz8/1) · [DriveIndia, arXiv 2507.19912](https://arxiv.org/abs/2507.19912v1) · [iWatchRoad / BharatPotHole, arXiv 2508.10945](https://arxiv.org/abs/2508.10945) · [Ali et al., WACV 2020 single-view distance](https://openaccess.thecvf.com/content_WACV_2020/papers/Ali_Real-time_vehicle_distance_estimation_using_single_view_geometry_WACV_2020_paper.pdf) · [Online extrinsic calibration for IPM with lane-width prior, arXiv 2008.03722](https://arxiv.org/pdf/2008.03722) · [OpenDRIVE from point clouds (lane width σ 0.22 m), arXiv 2405.07544](https://arxiv.org/pdf/2405.07544) · [Luo et al. 2018, horizontal curve from MMS (4.93 % radius error)](https://ascelibrary.com/doi/10.1061/%28ASCE%29SU.1943-5428.0000257) · [Ai & Tsai 2015, curve identification from GPS](https://www.bohrium.com/paper-details/automatic-horizontal-curve-identification-and-measurement-method-using-gps-data/814694627658432513-13367) · [Wood & Zhang 2018 smartphone curve radius thesis](https://openprairie.sdstate.edu/etd/1671/) · [Gupta et al., road grade from smartphones, IPSN 2020](https://arxiv.org/pdf/2006.03633) · [Ho et al., barometer altitude, MobiCom 2018](https://katalog.lib.cas.cz/KNAV/EdsRecord/edsair,edsair.doi...........9eaabaffdeaa111cd07a30e63b6713e5) · [Pothole area via YOLOv8 + IPM (9.71 % error)](https://www.researchgate.net/publication/388936793_A_Novel_Framework_for_Pothole_Area_Estimation_Based_on_Object_Detection_and_Monocular_Metric_Depth_Estimation) · [YOLOv8 ground-plane intersection for potholes](https://pmc.ncbi.nlm.nih.gov/articles/PMC13468935/) · [Depth Pro (Apple) baselines](https://arxiv.org/pdf/2410.02073) · [Depth Anything v1](https://arxiv.org/pdf/2401.10891) · [camera-trap depth comparison 2025](https://arxiv.org/html/2510.04723v1)

Ingest: [Geolocation metadata in iOS/Android video files (Addpipe)](https://blog.addpipe.com/geolocation-metadata-ios-android-video-files/) · [ExifTool forum: ©xyz / ISO6709 in MP4/MOV](https://exiftool.org/forum/index.php?msg=41874) · [AndroidX Media3 Mp4LocationData](https://developer.android.com/reference/androidx/media3/container/Mp4LocationData) · [GoPro GPMF sensor evolution (Trek View)](https://www.trekview.org/blog/evolution-of-gopro-camera-sensors-gpmf/) · [pygpmf-oz](https://pypi.org/project/pygpmf-oz) · [telemetrik](https://pypi.org/project/telemetrik/) · [gopro-overlay](https://pypi.org/project/gopro-overlay/) · [gopro2gpx](https://awesome.ecosyste.ms/projects/github.com%2Fjuanmcasillas%2Fgopro2gpx) · [gopro-telemetry (Node)](https://github.com/JuanIrache/gopro-telemetry) · [Mapillary forum: HERO13 GPS9 behaviour](https://forum.mapillary.com/t/gopro-hero-13-en-15-characters/8395)

Claude API: `claude-api` skill (model IDs, `messages.parse`, `output_config`, caching, batches) — Anthropic docs at platform.claude.com.
