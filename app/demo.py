import sys
from pathlib import Path
import gradio as gr
import torch
from torchvision.transforms.v2 import functional as TF

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.attention import explain_image, overlay_heatmap
from src.data import build_transform
from src.models import build_model
from PIL import Image

CHECKPOINT_DIR = PROJECT_ROOT / "outputs" / "checkpoints"

def check_checkpoint(filename):
    path = CHECKPOINT_DIR / filename
    if not path.is_file():
        raise FileNotFoundError(f"Thiếu checkpoint. Hãy đặt file tại: {path}")
    try:
        checkpoint = torch.load(path, map_location="cpu", weights_only=True)
        cfg = checkpoint["config"]
        names = checkpoint["class_names"]
        if len(names) != cfg["data"]["num_classes"]:
            raise ValueError("Số tên lớp không khớp config.")
        model = build_model(cfg)
        model.load_state_dict(checkpoint["model"], strict=True)
    except Exception as exc:
        raise ValueError(f"Checkpoint không hợp lệ: {path}. Hãy tải lại checkpoint đúng của mô hình.") from exc
    model.eval()
    return model, cfg, names


def predict_top5(model, image, cfg, class_names):
    """Trả về 5 tên lớp có xác suất cao nhất cho một ảnh PIL."""
    transform = build_transform(cfg, train=False)
    image_tensor = TF.to_image(image.convert("RGB"))
    image_tensor = TF.resize(image_tensor, [cfg["data"]["img_size"]] * 2, antialias=True)
    image_tensor = TF.to_dtype(image_tensor, torch.float32, scale=True)
    batch = transform(image_tensor).unsqueeze(0)

    model.eval()
    with torch.inference_mode():
        logits = model(batch)
        probabilities = torch.softmax(logits[0], dim=0)
        scores, indices = probabilities.topk(min(5, len(class_names)))

    return {class_names[index]: score
            for index, score in zip(indices.tolist(), scores.tolist())}

def create_demo():
    models = {
        run_name: check_checkpoint(f"{run_name}_best.pt")
        for run_name in ("vit_small_seed42", "cnn_baseline_seed42")
    }

    def predict_both(image):
        if not isinstance(image, Image.Image):
            raise gr.Error("Vui lòng chọn một file ảnh hợp lệ.")

        vit, vit_cfg, vit_classes = models["vit_small_seed42"]
        explanation = explain_image(vit, image, vit_cfg)

        scores, indices = explanation["logits"].softmax(dim=0).topk(min(5, len(vit_classes)))
        vit_top5 = {vit_classes[index]: score
                    for index, score in zip(indices.tolist(), scores.tolist())}
        rollout_image = overlay_heatmap(explanation["image"], explanation["rollout_map"])

        cnn, cnn_cfg, cnn_classes = models["cnn_baseline_seed42"]
        cnn_top5 = predict_top5(cnn, image, cnn_cfg, cnn_classes)

        return vit_top5, cnn_top5, rollout_image

    examples_dir = PROJECT_ROOT / "app" / "examples"
    examples = [
        [str(path)]
        for path in sorted(examples_dir.glob("*"))
        if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
    ]

    demo = gr.Interface(fn=predict_both,
                        inputs=gr.Image(type="pil", label="Ảnh đầu vào"),
                        outputs=[gr.Label(num_top_classes=5, label="ViT-small"),
                                 gr.Label(num_top_classes=5, label="CNN baseline"),
                                 gr.Image(type="pil", label="Attention rollout của ViT"),],
                        examples=examples,
                        flagging_mode = "never",
                        title="Phân loại ảnh Tiny ImageNet",)
    return demo


def main():
    try:
        demo = create_demo()
    except (FileNotFoundError, ValueError) as exc:
        print(f"Không thể mở demo: {exc}", file=sys.stderr)
        return 1
    demo.launch()
    return 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    raise SystemExit(main())
