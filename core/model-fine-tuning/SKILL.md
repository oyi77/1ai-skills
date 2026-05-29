---
name: model-fine-tuning
description: Fine-tune LLMs and ML models — LoRA, QLoRA, PEFT, Hugging Face. Dataset prep, training, evaluation, deployment
---

## Overview

Fine-tune pre-trained models for specific tasks. Covers LoRA/QLoRA for efficient training, dataset preparation, evaluation, and deployment of custom models.

## Capabilities

- Fine-tune LLMs with LoRA and QLoRA (low-rank adaptation)
- Prepare datasets in instruction/chat format
- Use Hugging Face Transformers + PEFT for training
- Evaluate fine-tuned models with benchmarks
- Merge LoRA adapters back into base models
- Deploy fine-tuned models via vLLM or Ollama

## When to Use

- Need a model specialized for a specific domain (legal, medical, code)
- Want better performance on specific tasks than general models
- Have domain-specific data that improves with training
- Need to reduce model size while maintaining quality
- Building a product that needs a custom AI model

## Pseudo Code
```python
# Example workflow for this skill
def execute(input_data):
    # Step 1: Validate input
    if not input_data:
        raise ValueError("Input data is required")

    # Step 2: Process core logic
    result = process(input_data)

    # Step 3: Validate output
    validate_output(result)

    return result
```


### Dataset Preparation (Hugging Face Format)
```python
from datasets import Dataset

# Instruction format
data = [
    {"instruction": "Summarize this text", "input": "Long article...", "output": "Summary..."},
    {"instruction": "Translate to French", "input": "Hello world", "output": "Bonjour le monde"},
]

# Chat format (for chat models)
data = [
    {"messages": [
        {"role": "system", "content": "You are a legal assistant."},
        {"role": "user", "content": "What is a contract?"},
        {"role": "assistant", "content": "A contract is a legally binding agreement..."}
    ]},
]

dataset = Dataset.from_list(data)
dataset.push_to_hub("username/my-dataset")
```

### LoRA Fine-Tuning (Hugging Face + PEFT)
```python
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from peft import LoraConfig, get_peft_model
from trl import SFTTrainer

# Load base model
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B-Instruct",
    torch_dtype="auto",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")

# Configure LoRA
lora_config = LoraConfig(
    r=16,                    # Rank (8-64)
    lora_alpha=32,           # Alpha scaling
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)

# Training
training_args = TrainingArguments(
    output_dir="./output",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    warmup_steps=100,
    logging_steps=10,
    save_steps=500,
    bf16=True,
    optim="paged_adamw_8bit"
)

trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    tokenizer=tokenizer,
    max_seq_length=2048
)

trainer.train()
trainer.save_model("./final-model")
```

### QLoRA (4-bit Quantized Training)
```python
from transformers import BitsAndBytesConfig
import torch

# 4-bit quantization config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True
)

# Load model in 4-bit
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B-Instruct",
    quantization_config=bnb_config,
    device_map="auto"
)

# Then apply LoRA as above — uses ~6GB VRAM instead of ~16GB
```

### Merge LoRA Adapter
```python
from peft import PeftModel

# Load base + adapter
base_model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")
model = PeftModel.from_pretrained(base_model, "./final-model")

# Merge
merged_model = model.merge_and_unload()
merged_model.save_pretrained("./merged-model")
tokenizer.save_pretrained("./merged-model")

# Push to Hub
merged_model.push_to_hub("username/my-fine-tuned-model")
tokenizer.push_to_hub("username/my-fine-tuned-model")
```

### Evaluate Model
```python
import lm_eval

results = lm_eval.simple_evaluate(
    model="hf",
    model_args="pretrained=./merged-model",
    tasks=["mmlu", "hellaswag", "arc_challenge"],
    batch_size=8
)

print(results["results"])
```

### Deploy with Ollama
```bash
# Create Modelfile
cat > Modelfile << 'EOF'
FROM ./merged-model
PARAMETER temperature 0.7
PARAMETER top_p 0.9
SYSTEM "You are a specialized legal assistant."
EOF

# Build and run
ollama create my-legal-model -f Modelfile
ollama run my-legal-model
```

## Common Patterns
- Use structured input/output schemas for reliable automation
- Add retry logic with exponential backoff for external calls
- Validate inputs before processing to fail fast
- Log execution steps for debugging and auditing


### Training Data Quality Checklist
```
- 100-1000 examples minimum for LoRA
- Consistent format across all examples
- No duplicate or near-duplicate entries
- Balanced representation of target tasks
- Clean, well-formatted outputs
```

### LoRA Hyperparameter Guide
```
r=8:   Simple tasks, minimal data
r=16:  Standard choice, good balance
r=32:  Complex tasks, more data
r=64:  Maximum capacity, risk of overfitting

learning_rate: 1e-4 to 3e-4 (lower for larger models)
epochs: 1-3 (more risks overfitting on small datasets)
batch_size: As large as VRAM allows
```

### VRAM Requirements (QLoRA 4-bit)
```
7B:   ~6GB VRAM  → RTX 3060 12GB works
13B:  ~10GB VRAM → RTX 3080 10GB works
70B:  ~36GB VRAM → A100 40GB or 2x RTX 4090
```

## How to Use

1. Invoke the skill when relevant domain keywords appear in the request
2. Provide required inputs as specified in the skill definition
3. Review the output for correctness before delivering to the user
4. Combine with related skills for complex multi-step workflows

## Verification

After completing this skill, confirm:

- [ ] Output meets the defined quality and completeness requirements
- [ ] All prerequisites are verified and documented
- [ ] Error handling covers edge cases
- [ ] Results are accurate and actionable
