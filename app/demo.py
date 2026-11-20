from pathlib import Path
import torch
import gradio as gr
from src.data import build_transform
from PIL import Image
from src.models import build_model
from torchvision.transforms.v2 import functional as TF
from src.attention import explain_image, overlay_heatmap

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHECKPOINT_DIR = PROJECT_ROOT / "outputs" / "checkpoints"

def check_checkpoint(filename):
    path = CHECKPOINT_DIR / filename
    if not path.is_file():
        raise FileNotFoundError(f"Thiếu checkpoint. Hãy đặt file tại: {path}")

    checkpoint = torch.load(path, map_location="cpu", weights_only=True)
    data_cfg = checkpoint["config"]["data"]
    class_names = checkpoint["class_names"]

    print(f"\n{filename}")
    print(f"Số lớp: {len(class_names)}")
    print(f"Ba lớp đầu: {class_names[:3]}")
    print(f"Kích thước ảnh: {data_cfg['img_size']}")
    print(f"Mean: {data_cfg['mean']}")
    print(f"Std:  {data_cfg['std']}")

def predict_top5(model, image, cfg, class_names):
    """Trả về 5 tên lớp có xác suất cao nhất cho một ảnh PIL."""
    transform = build_transform(cfg, train=False)
    image_tensor = TF.to_image(image.convert("RGB"))
    image_tensor = TF.resize(image_tensor, [64, 64], antialias=True) 
    image_tensor = TF.to_dtype(image_tensor, torch.float32, scale=True)
    batch = transform(image_tensor).unsqueeze(0)

    model.eval()
    with torch.inference_mode():
        logits = model(batch)
        probabilities = torch.softmax(logits[0], dim=0)
        scores, indices = probabilities.topk(5)

    return {class_names[index]: score 
            for index, score in zip(indices.tolist(), scores.tolist())}

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    checkpoint_dir = root / "outputs" / "checkpoints"

    models = {}
    for run_name in ("vit_small_seed42", "cnn_baseline_seed42"):
        checkpoint = torch.load(checkpoint_dir / f"{run_name}_best.pt", 
                                map_location="cpu",
                                weights_only=True,
                                )
        cfg = checkpoint["config"]
        model = build_model(cfg)
        model.load_state_dict(checkpoint["model"])
        model.eval()
        models[run_name] = (model, cfg, checkpoint["class_names"])

    def predict_both(image):
        if image is None:
            raise gr.Error("Vui lòng chọn một ảnh.")

        vit, vit_cfg, vit_classes = models["vit_small_seed42"]
        explanation = explain_image(vit, image, vit_cfg)

        scores, indices = explanation["logits"].softmax(dim=0).topk(5)
        vit_top5 = {vit_classes[index]: score 
                    for index, score in zip(indices.tolist(), scores.tolist())}
        rollout_image = overlay_heatmap(explanation["image"], explanation["rollout_map"])

        cnn, cnn_cfg, cnn_classes = models["cnn_baseline_seed42"]
        cnn_top5 = predict_top5(cnn, image, cnn_cfg, cnn_classes)

        return vit_top5, cnn_top5, rollout_image

    examples_dir = root / "app" / "examples"
    examples = [
        [str(path)]
        for path in sorted(examples_dir.iterdir())
        if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
    ]
    
    demo = gr.Interface(fn=predict_both, 
                        inputs=gr.Image(type="pil", label="Ảnh đầu vào"),
                        outputs=[gr.Label(num_top_classes=5, label="ViT-small"),
                                 gr.Label(num_top_classes=5, label="CNN baseline"),
                                 gr.Image(type="pil", label="Attention rollout của ViT"),], 
                        examples=examples,
                        flagging_mode="never",
                        title="Phân loại ảnh Tiny ImageNet",)
    demo.launch()