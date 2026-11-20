import torch
from src.models import build_model
import csv
import json
from pathlib import Path
from src.data import build_loader
from time import perf_counter

def load_model_for_evaluation(checkpoint_path, device):
    checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=True)
    cfg = checkpoint["config"]
    model = build_model(cfg)
    model.load_state_dict(checkpoint["model"], strict= True)
    model.to(device)
    model.eval()
    return model, cfg

def evaluate_model(model, loader, device):
    total = 0
    correct_top1 = 0
    correct_top5 = 0
    predictions = []
    per_class = {}

    model.eval()
    with torch.inference_mode():
        for images, labels in loader:
            images = images.to(device)
            labels = labels.to(device)

            logits = model(images)
            k = min(5, logits.shape[1])
            top_indices = logits.topk(k, dim=1).indices

            pred_top1 = top_indices[:, 0]
            top1_matches = pred_top1 == labels
            top5_matches = (top_indices == labels.unsqueeze(1)).any(dim=1)

            batch_size = labels.size(0)
            correct_top1 += top1_matches.sum().item()
            correct_top5 += top5_matches.sum().item()

            confidence = logits.softmax(dim=1).gather(1, pred_top1.unsqueeze(1))
            confidence = confidence.squeeze(1).cpu().tolist()

            true_labels = labels.cpu().tolist()
            pred_labels = pred_top1.cpu().tolist()

            for i, (true_label, pred_label) in enumerate(zip(true_labels, pred_labels)):
                if true_label not in per_class:
                    per_class[true_label] = {"total": 0, "correct": 0}

                per_class[true_label]["total"] += 1
                if pred_label == true_label:
                    per_class[true_label]["correct"] += 1

                predictions.append({"image_index": total + i,
                                    "true_label": true_label,
                                    "pred_label": pred_label,
                                    "confidence": confidence[i],})
            total += batch_size

    if total == 0:
        raise ValueError("Tập test không có ảnh để đánh giá.")

    metrics = {"top1": 100 * correct_top1 / total,
               "top5": 100 * correct_top5 / total,}

    for counts in per_class.values():
        counts["accuracy_pct"] = 100 * counts["correct"] / counts["total"]

    return metrics, per_class, predictions

def save_results(run_name, metrics, per_class, predictions):
    results_dir = Path("outputs/results")
    results_dir.mkdir(parents=True, exist_ok=True)
    class_names_path = results_dir / "class_names.json"
    class_names = json.loads(class_names_path.read_text(encoding="utf-8"))

    summary = {"run_name": run_name,
               "model": metrics["model"],
               "seed": metrics["seed"],
               "params": metrics["params"],
               "macs": metrics.get("macs"),
               "top1": metrics["top1"],
               "top5": metrics["top5"],
               "epoch_time_s": metrics.get("epoch_time_s"),
               "inference_img_per_s": metrics.get("inference_img_per_s"),
               "peak_vram_mb": metrics.get("peak_vram_mb"),}

    with (results_dir / f"{run_name}.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    per_class_path = results_dir / f"{run_name}_per_class.csv"
    with per_class_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["class_id", "class_name", "correct", "total", "accuracy_pct"])

        for class_id, class_name in enumerate(class_names):
            counts = per_class.get(class_id)
            if counts is None:
                writer.writerow([class_id, class_name, 0, 0, None])
            else:
                writer.writerow([class_id, class_name, counts["correct"],
                                 counts["total"], counts["accuracy_pct"],])

    predictions_path = results_dir / f"{run_name}_predictions.csv"
    with predictions_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["image_index", "true_label", 
                                               "pred_label", "confidence"],)
        writer.writeheader()
        writer.writerows(predictions)

def measure_inference_speed(model, images, repeats=10):
    model.eval()
    with torch.inference_mode():
        for _ in range(3):
            model(images)

        start = perf_counter()
        for _ in range(repeats):
            model(images)
        elapsed = perf_counter() - start

    return images.size(0) * repeats / elapsed

def update_inference_speeds():
    from src.data import build_loader

    results_dir = Path("outputs/results")
    checkpoint_dir = Path("outputs/checkpoints")
    images = None

    for run_name in ("vit_small_seed42", "cnn_baseline_seed42"):
        result_path = results_dir / f"{run_name}.json"
        result = json.loads(result_path.read_text(encoding="utf-8"))

        checkpoint_path = checkpoint_dir / f"{run_name}_best.pt"
        model, cfg = load_model_for_evaluation(checkpoint_path, device="cpu")

        if images is None:
            cfg["data"].update(batch_size=64, num_workers=0)
            images, _ = next(iter(build_loader(cfg, "val")))

        speed = measure_inference_speed(model, images)
        result["inference_img_per_s"] = speed
        result_path.write_text(
            json.dumps(result, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        print(f"{run_name}: {speed:.2f} ảnh/giây (CPU, batch {images.size(0)})")

def main():
    device = "cpu"
    checkpoints = {"vit_small_seed42": "outputs/checkpoints/vit_small_seed42_best.pt",
                   "cnn_baseline_seed42": "outputs/checkpoints/cnn_baseline_seed42_best.pt",}

    for run_name, checkpoint_path in checkpoints.items():
        model, cfg = load_model_for_evaluation(checkpoint_path, device)        
        loader = build_loader(cfg, "test")
        metrics, per_class, predictions = evaluate_model(model, loader, device)
        metrics.update({"model": cfg["model"]["name"], "seed": cfg["seed"],
                        "params": sum(p.numel() for p in model.parameters()),})        
        save_results(run_name, metrics, per_class, predictions)

if __name__ == "__main__":
    main()
