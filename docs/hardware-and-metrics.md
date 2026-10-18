# Initial consumer-compute envelope

Target Fedora laptop (i7-10750H, 32 GiB RAM, RTX 3060 Laptop GPU with 6 GiB VRAM). These are configuration targets from project context, **not measured experimental results**.

Every run should record CPU/GPU model, driver, CUDA/ONNX/runtime version, RAM/VRAM free and peak, precision/quantization, batch, context length, prompt tokens, generation tokens, tokenizer time, first-token latency, tokens/sec, total latency, warm/cold load and model residency, energy measurement source if any.

Compare end-to-end cost per correct task under explicit maximum resource budgets. Beware simultaneous model residency, GPU fragmentation, thermal throttling, and CPU/GPU transfer.
