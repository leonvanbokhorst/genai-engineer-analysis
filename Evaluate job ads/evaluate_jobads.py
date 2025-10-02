
import json, math, collections
from typing import List, Dict, Tuple

def load_jsonl(path: str) -> Dict[str, dict]:
    data = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            obj = json.loads(line)
            data[obj["doc_id"]] = obj
    return data

def percent_agreement(y_true: list, y_pred: list) -> float:
    assert len(y_true) == len(y_pred)
    if not y_true:
        return 0.0
    agree = sum(1 for a, b in zip(y_true, y_pred) if a == b)
    return agree / len(y_true)

def cohen_kappa(y_true: list, y_pred: list) -> float:
    # Multiclass Cohen's kappa via confusion matrix
    labels = sorted(set(y_true) | set(y_pred))
    index = {l:i for i,l in enumerate(labels)}
    n = len(labels)
    cm = [[0]*n for _ in range(n)]
    for a,b in zip(y_true, y_pred):
        cm[index[a]][index[b]] += 1
    total = sum(sum(row) for row in cm) or 1
    po = sum(cm[i][i] for i in range(n)) / total
    # expected agreement
    row_marg = [sum(cm[i][j] for j in range(n)) for i in range(n)]
    col_marg = [sum(cm[i][j] for i in range(n)) for j in range(n)]
    pe = sum((row_marg[i]*col_marg[i]) for i in range(n)) / (total*total)
    denom = (1 - pe) if (1 - pe) != 0 else 1e-12
    kappa = (po - pe) / denom
    return kappa

def iou(a_start:int, a_end:int, b_start:int, b_end:int) -> float:
    inter = max(0, min(a_end, b_end) - max(a_start, b_start))
    union = max(a_end, b_end) - min(a_start, b_start)
    if union == 0:
        return 0.0
    return inter / union

def stage1_span_metrics(gold_spans: List[dict], pred_spans: List[dict], iou_thresh: float = 0.5) -> Dict[str, float]:
    # A predicted span is a True Positive if there exists a gold span with IoU>=0.5 AND same code.
    # Remaining predicted spans are False Positives; remaining gold spans are False Negatives.
    matched_gold = set()
    tp = 0
    for pi, p in enumerate(pred_spans):
        best = -1
        best_iou = 0.0
        for gi, g in enumerate(gold_spans):
            if gi in matched_gold:
                continue
            if p.get("code") != g.get("code"):
                continue
            i = iou(p["start"], p["end"], g["start"], g["end"])
            if i >= iou_thresh and i > best_iou:
                best_iou = i
                best = gi
        if best >= 0:
            tp += 1
            matched_gold.add(best)
    fp = max(0, len(pred_spans) - tp)
    fn = max(0, len(gold_spans) - tp)
    prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2*prec*rec / (prec+rec) if (prec+rec) > 0 else 0.0
    return {"precision": prec, "recall": rec, "f1": f1, "tp": tp, "fp": fp, "fn": fn}

def confusion_matrix(y_true: list, y_pred: list) -> Dict[str, dict]:
    labels = sorted(set(y_true) | set(y_pred))
    idx = {l:i for i,l in enumerate(labels)}
    n = len(labels)
    cm = [[0]*n for _ in range(n)]
    for a,b in zip(y_true, y_pred):
        cm[idx[a]][idx[b]] += 1
    out = {"labels": labels, "matrix": cm}
    return out

def evaluate(gold_path: str, pred_path: str, iou_thresh: float = 0.5) -> dict:
    gold = load_jsonl(gold_path)
    pred = load_jsonl(pred_path)
    # align
    keys = sorted(set(gold.keys()) & set(pred.keys()))
    if not keys:
        raise ValueError("No overlapping doc_id between gold and predictions.")
    # Stage 0
    y0_true = [bool(gold[k]["stage0"]["relevant"]) for k in keys]
    y0_pred = [bool(pred[k]["stage0"]["relevant"]) for k in keys]
    stage0 = {
        "n": len(keys),
        "percent_agreement": percent_agreement(y0_true, y0_pred),
        "cohen_kappa": cohen_kappa(y0_true, y0_pred)
    }
    # Stage 1 (micro-avg across docs)
    tp=fp=fn=0
    for k in keys:
        gsp = gold[k].get("stage1", {}).get("spans", [])
        psp = pred[k].get("stage1", {}).get("spans", [])
        m = stage1_span_metrics(gsp, psp, iou_thresh=iou_thresh)
        tp += m["tp"]; fp += m["fp"]; fn += m["fn"]
    prec = tp/(tp+fp) if (tp+fp)>0 else 0.0
    rec = tp/(tp+fn) if (tp+fn)>0 else 0.0
    f1 = 2*prec*rec/(prec+rec) if (prec+rec)>0 else 0.0
    stage1 = {"precision": prec, "recall": rec, "f1": f1, "tp": tp, "fp": fp, "fn": fn, "iou_thresh": iou_thresh}
    # Stage 2
    y2_true = [gold[k]["stage2"]["label"] for k in keys]
    y2_pred = [pred[k]["stage2"]["label"] for k in keys]
    stage2 = {
        "n": len(keys),
        "percent_agreement": percent_agreement(y2_true, y2_pred),
        "cohen_kappa": cohen_kappa(y2_true, y2_pred),
        "confusion_matrix": confusion_matrix(y2_true, y2_pred)
    }
    return {"n_docs": len(keys), "stage0": stage0, "stage1": stage1, "stage2": stage2}

def save_report(res: dict, path: str):
    labels = res["stage2"]["confusion_matrix"]["labels"]
    mat = res["stage2"]["confusion_matrix"]["matrix"]
    lines = []
    lines.append(f"Docs: {res['n_docs']}")
    lines.append("")
    lines.append("Stage 0 — Relevance")
    lines.append(f"  Percent agreement: {res['stage0']['percent_agreement']:.2f}")
    lines.append(f"  Cohen's kappa:    {res['stage0']['cohen_kappa']:.2f}")
    lines.append("")
    lines.append("Stage 1 — Feature extraction (span, micro-avg)")
    lines.append(f"  Precision: {res['stage1']['precision']:.2f}")
    lines.append(f"  Recall:    {res['stage1']['recall']:.2f}")
    lines.append(f"  F1:        {res['stage1']['f1']:.2f}")
    lines.append(f"  (tp={res['stage1']['tp']}, fp={res['stage1']['fp']}, fn={res['stage1']['fn']}, IoU≥{res['stage1']['iou_thresh']})")
    lines.append("")
    lines.append("Stage 2 — Final classification")
    lines.append(f"  Percent agreement: {res['stage2']['percent_agreement']:.2f}")
    lines.append(f"  Cohen's kappa:     {res['stage2']['cohen_kappa']:.2f}")
    # confusion matrix
    col_width = max(10, max(len(x) for x in labels))
    header = " " * (col_width+2) + " | " + " | ".join([f"{l:>{col_width}}" for l in labels]) + " |"
    lines.append("")
    lines.append("  Confusion matrix (rows=human, cols=LLM)")
    lines.append("  " + header)
    for i, row in enumerate(mat):
        row_total = sum(row)
        row_str = f"{labels[i]:>{col_width}}  | " + " | ".join([f"{v:>{col_width}d}" for v in row]) + " |"
        lines.append("  " + row_str + f"   (n={row_total})")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--gold", required=True)
    ap.add_argument("--pred", required=True)
    ap.add_argument("--iou", type=float, default=0.5)
    ap.add_argument("--out_json", default="eval_result.json")
    ap.add_argument("--out_txt", default="eval_report.txt")
    args = ap.parse_args()
    res = evaluate(args.gold, args.pred, iou_thresh=args.iou)
    with open(args.out_json, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2)
    save_report(res, args.out_txt)

if __name__ == "__main__":
    main()
