import csv
import json
from collections import Counter
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np


def save_top_confusions(run_name, results_dir, class_names):
    """Đếm 20 cặp nhãn thật → nhãn dự đoán sai nhiều nhất."""
    counts = Counter()
    predictions_path = results_dir / f"{run_name}_predictions.csv"

    with predictions_path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            true_id = int(row["true_label"])
            pred_id = int(row["pred_label"])

            if true_id != pred_id:
                counts[(true_id, pred_id)] += 1

    output_path = results_dir / f"{run_name}_top20_confusions.csv"
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["true_label", "true_name", "pred_label", "pred_name", "count"])

        for (true_id, pred_id), count in counts.most_common(20):
            writer.writerow([
                true_id, class_names[true_id],
                pred_id, class_names[pred_id],
                count,
            ])

    print(f"{run_name}: {sum(counts.values())} ảnh sai. Đã lưu {output_path}")

def save_confusion_heatmap(run_name, results_dir, class_names):
    num_classes = len(class_names)
    matrix = np.zeros((num_classes, num_classes), dtype=int)

    predictions_path = results_dir / f"{run_name}_predictions.csv"
    with predictions_path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            true_id = int(row["true_label"])
            pred_id = int(row["pred_label"])
            matrix[true_id, pred_id] += 1

    figures_dir = Path("outputs/figures")
    figures_dir.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(9, 8))
    heatmap = ax.imshow(
        matrix, cmap="Blues", interpolation="nearest", vmin=0, vmax=50
    )
    ax.set_title(f"Confusion matrix – {run_name}")
    ax.set_xlabel("Predicted class ID")
    ax.set_ylabel("True class ID")
    fig.colorbar(heatmap, ax=ax, label="Number of images")

    output_path = figures_dir / f"confusion_{run_name}.png"
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)

    print(f"{run_name}: {matrix.sum()} ảnh, {matrix.trace()} ảnh đúng")

def save_error_grid(run_name, results_dir, class_names, test_images):
    predictions_path = results_dir / f"{run_name}_predictions.csv"

    with predictions_path.open(encoding="utf-8", newline="") as f:
        wrong_rows = [
            row for row in csv.DictReader(f)
            if row["true_label"] != row["pred_label"]
        ]

    rng = np.random.default_rng(42)
    selected = rng.choice(len(wrong_rows), size=20, replace=False)

    fig, axes = plt.subplots(4, 5, figsize=(15, 12), layout="constrained")
    fig.suptitle(f"20 misclassified test images – {run_name}", fontsize=16)

    for ax, row_index in zip(axes.flat, selected):
        row = wrong_rows[row_index]
        image_index = int(row["image_index"])
        true_name = class_names[int(row["true_label"])]
        pred_name = class_names[int(row["pred_label"])]
        confidence = float(row["confidence"])

        ax.imshow(test_images[image_index])
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlabel(
            f"True: {true_name}\nPred: {pred_name} ({confidence:.1%})",
            fontsize=9,
        )

    figures_dir = Path("outputs/figures")
    figures_dir.mkdir(parents=True, exist_ok=True)
    output_path = figures_dir / f"errors_{run_name}.png"
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Đã lưu {output_path}")

def save_class_ranking(run_name, results_dir):
    input_path = results_dir / f"{run_name}_per_class.csv"
    with input_path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    ranked = sorted(rows, key=lambda row: float(row["accuracy_pct"]), reverse=True)

    output_path = results_dir / f"{run_name}_class_ranking.csv"
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["group", "rank", "class_name", "correct", "total", "accuracy_pct"])

        for group, selected in [("best", ranked[:10]), ("worst", ranked[-10:][::-1])]:
            for rank, row in enumerate(selected, start=1):
                writer.writerow([
                    group, rank, row["class_name"],
                    row["correct"], row["total"], row["accuracy_pct"],
                ])

    print(f"Đã lưu {output_path}")

def main():
    results_dir = Path("outputs/results")
    class_names = json.loads(
        (results_dir / "class_names.json").read_text(encoding="utf-8")
    )

    for run_name in ("vit_small_seed42", "cnn_baseline_seed42"):
        save_top_confusions(run_name, results_dir, class_names)

    for run_name in ("vit_small_seed42", "cnn_baseline_seed42"):
        save_top_confusions(run_name, results_dir, class_names)
        save_confusion_heatmap(run_name, results_dir, class_names)

        test_images = np.load("data/cache/tiny_imagenet_64/test_x.npy", mmap_mode="r")

    for run_name in ("vit_small_seed42", "cnn_baseline_seed42"):
        save_top_confusions(run_name, results_dir, class_names)
        save_confusion_heatmap(run_name, results_dir, class_names)
        save_error_grid(run_name, results_dir, class_names, test_images)
        save_class_ranking(run_name, results_dir)  

if __name__ == "__main__":
    main()