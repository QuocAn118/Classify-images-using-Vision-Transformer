import csv
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def load_result(results_dir, run_name):
    """Đọc kết quả đánh giá của một lần chạy."""
    path = results_dir / f"{run_name}.json"

    with path.open(encoding="utf-8") as f:
        return json.load(f)

def save_comparison_csv(results_dir, rows):
    """Ghi một dòng cho mỗi mô hình, theo cùng thứ tự cột."""
    columns = ["run_name", "model", "seed", "params", "flops_per_image", "macs",
        "top1", "top5", "epoch_time_s", "inference_img_per_s", "peak_vram_mb",
    ]
    path = results_dir / "comparison.csv"

    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()

        for row in rows:
            writer.writerow({
                column: "chưa có" if row.get(column) is None else row[column]
                for column in columns
            })

    print(f"Đã lưu {path}")

def save_comparison_markdown(results_dir):
    """Chuyển bảng comparison.csv thành bảng Markdown."""
    csv_path = results_dir / "comparison.csv"
    md_path = results_dir / "comparison.md"

    with csv_path.open(encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        lines = [
            "# So sánh ViT và CNN",
            "",
            "| " + " | ".join(header) + " |",
            "| " + " | ".join(["---"] * len(header)) + " |",
        ]

        for row in reader:
            lines.append("| " + " | ".join(row) + " |")

    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Đã lưu {md_path}")

def save_comparison_plots(rows):
    figures_dir = Path("outputs/figures")
    figures_dir.mkdir(parents=True, exist_ok=True)

    model_names = {"vit": "ViT-small", "resnet_small": "CNN baseline"}
    colors = {"vit": "#3066BE", "resnet_small": "#C55A11"}


    fig, ax = plt.subplots(figsize=(6, 4))
    names = [model_names[row["model"]] for row in rows]
    scores = [row.get("top1") for row in rows]
    bars = ax.bar(names, [0 if score is None else score for score in scores],
                  color=[colors[row["model"]] for row in rows])
    ax.bar_label(bars, labels=["chưa có" if score is None else f"{score:.2f}%"
                              for score in scores], padding=4)
    ax.set(title="Top-1 trên tập test", ylabel="Top-1 (%)", ylim=(0, 100))
    fig.tight_layout()
    fig.savefig(figures_dir / "comparison_test_top1.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4))
    for row in rows:
        log_path = Path("outputs/logs") / f"{row['run_name']}.csv"
        if not log_path.is_file():
            continue
        with log_path.open(encoding="utf-8", newline="") as f:
            history = list(csv.DictReader(f))

        epochs = [int(entry["epoch"]) for entry in history]
        val_scores = [float(entry["val_top1"]) for entry in history]
        model = row["model"]
        ax.plot(epochs, val_scores, label=model_names[model], color=colors[model])

    ax.set(title="Top-1 trên tập validation theo epoch",
           xlabel="Epoch", ylabel="Validation Top-1 (%)")
    if ax.lines:
        ax.legend()
    else:
        ax.text(0.5, 0.5, "Chưa có log huấn luyện", ha="center", transform=ax.transAxes)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(figures_dir / "comparison_val_top1.png", dpi=160)
    plt.close(fig)

def main():
    results_dir = Path("outputs/results")

    model_checks = (load_result(results_dir, "task005_cnn_checks").get("models", {})
                    if (results_dir / "task005_cnn_checks.json").is_file() else {})
    training_runs = (load_result(results_dir, "task011_training_checks").get("runs", [])
                     if (results_dir / "task011_training_checks.json").is_file() else [])
    training_by_name = {run["run_name"]: run for run in training_runs}

    rows = []
    for run_name in ("vit_small_seed42", "cnn_baseline_seed42"):
        result = load_result(results_dir, run_name)
        training = training_by_name.get(run_name, {})
        model_key = "vit_small" if result["model"] == "vit" else result["model"]

        row = {
            "run_name": run_name,
            "model": result["model"],
            "seed": result["seed"],
            "params": result["params"],
            "flops_per_image": model_checks.get(model_key, {}).get("flops"),
            "macs": result.get("macs"),
            "top1": result.get("top1"),
            "top5": result.get("top5"),
            "epoch_time_s": training.get("mean_epoch_time_s", result.get("epoch_time_s")),
            "inference_img_per_s": result.get("inference_img_per_s"),
            "peak_vram_mb": training.get("peak_allocated_vram_mb", result.get("peak_vram_mb")),
        }
        rows.append(row)

    save_comparison_csv(results_dir, rows)
    save_comparison_markdown(results_dir)
    save_comparison_plots(rows)

if __name__ == "__main__":
    main()
