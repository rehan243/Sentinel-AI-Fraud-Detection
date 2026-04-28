#!/usr/bin/env bash
# retrain fraud model, compare to holdout, optionally promote artifact
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

usage() {
  echo "usage: $0 [--promote]"
}

PROMOTE=0
for arg in "$@"; do
  case "$arg" in
    --promote) PROMOTE=1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo -e "${RED}unknown:${NC} $arg"; usage; exit 1 ;;
  esac
done

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ -f .venv/bin/activate ]]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

DATA="${TRAIN_TABLE:-fraud.training_features}"
HOLDOUT="${HOLDOUT_TABLE:-fraud.holdout_features}"
MODEL_DIR="${MODEL_DIR:-artifacts/fraud_model}"

echo -e "${GREEN}training${NC} on $DATA"
python -m fraud_train --data "$DATA" --out "$MODEL_DIR" || {
  echo -e "${RED}train failed${NC}"; exit 1
}

echo -e "${GREEN}validating${NC} on $HOLDOUT"
METRIC="$(python -m fraud_eval --model "$MODEL_DIR" --data "$HOLDOUT" | tail -n 1)"
echo -e "${YELLOW}metric line:${NC} $METRIC"

if [[ "$PROMOTE" -eq 1 ]]; then
  echo -e "${GREEN}promoting (stub copy)${NC}"
  mkdir -p promoted
  cp -r "$MODEL_DIR" promoted/model_"$(date +%s)"
fi

echo -e "${GREEN}retrain flow done${NC}"
