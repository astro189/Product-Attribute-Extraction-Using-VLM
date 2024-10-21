import torch
from transformers import AutoTokenizer, AutoProcessor, TrainingArguments, LlavaForConditionalGeneration, BitsAndBytesConfig
from trl import SFTTrainer
from peft import LoraConfig

from transformers import AutoProcessor
import torch
from PIL import Image
from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM

class LLavaDataCollator:
    def __init__(self, processor):
        self.processor = processor

    def __call__(self, examples):
        texts = []
        images = []

        for idx, example in enumerate(examples):
            try:
                text = self.processor.tokenizer.apply_chat_template(
                    example["messages"], 
                    tokenize=False, 
                    add_generation_prompt=False
                )

                if len(example["images"]) > 0:
                    image = example["images"][0] 
                    images.append(image)
                else:
                    print(f"Warning: No image found in example {idx}. Check your dataset.")
                    images.append(None)  

                texts.append(text)
                
            except Exception as e:
                print(f"Error processing example {idx}: {example}")
                print(f"Exception: {e}")
                continue 


        try:
            batch = self.processor(
                text=texts,
                images=images,
                return_tensors="pt",
                padding=True,
            )
            
            labels = batch["input_ids"].clone()
            if self.processor.tokenizer.pad_token_id is not None:
                labels[labels == self.processor.tokenizer.pad_token_id] = -100
            batch["labels"] = labels

        except Exception as e:
            print("Error occurred while creating the batch:")
            print(f"Texts: {texts}")
            print(f"Images: {images}")
            print(f"Exception: {e}")
            raise  # Re-raise the exception to stop the training process for debugging

        return batch
    

def init_base_model():
    model_id = "llava-hf/llava-1.5-7b-hf"

    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
    )

    base_model = LlavaForConditionalGeneration.from_pretrained(model_id,
                                                        quantization_config=quantization_config,
                                                        torch_dtype=torch.float16)


    LLAVA_CHAT_TEMPLATE = """A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions. {% for message in messages %}{% if message['role'] == 'user' %}USER: {% else %}ASSISTANT: {% endif %}{% for item in message['content'] %}{% if item['type'] == 'text' %}{{ item['text'] }}{% elif item['type'] == 'image' %}<image>{% endif %}{% endfor %}{% if message['role'] == 'user' %} {% else %}{{eos_token}}{% endif %}{% endfor %}"""

    tokenizer = AutoTokenizer.from_pretrained(model_id)
    tokenizer.chat_template = LLAVA_CHAT_TEMPLATE
    processor = AutoProcessor.from_pretrained(model_id)
    processor.tokenizer = tokenizer

    return base_model, processor


def init_fine_tuned_model():
    base_model = init_base_model()
    processor = AutoProcessor.from_pretrained("llava-hf/llava-1.5-13b-hf")
    LLAVA_CHAT_TEMPLATE = """A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions. {% for message in messages %}{% if message['role'] == 'user' %}USER: {% else %}ASSISTANT: {% endif %}{% for item in message['content'] %}{% if item['type'] == 'text' %}{{ item['text'] }}{% elif item['type'] == 'image' %}<image>{% endif %}{% endfor %}{% if message['role'] == 'user' %} {% else %}{{eos_token}}{% endif %}{% endfor %}"""
    processor.tokenizer.chat_template = LLAVA_CHAT_TEMPLATE

    config = PeftConfig.from_pretrained("astro189/working")
    model_tuned = PeftModel.from_pretrained(base_model, "astro189/working")
    return model_tuned, processor

def generate_response(image_path, prompt):
    model_tuned, processor = init_fine_tuned_model()
    
    data_collator = LLavaDataCollator(processor)
    image = Image.open(image_path)
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image", "image": None}
            ]
        }
    ]
   
    text = processor.tokenizer.apply_chat_template(messages, tokenize=False)

    model_inputs = processor(
        images=image,
        text=text,
        return_tensors="pt",
        padding=True
    )

    with torch.no_grad():
        outputs = model_tuned.generate(
            **model_inputs,
            max_new_tokens=128,
            do_sample=False
        )

    response = processor.tokenizer.decode(outputs[0], skip_special_tokens=True)
    response = response.split("ASSISTANT:")[-1].strip()
    return response

if __name__ == "___main__":
    image_path = ".IMAGES/005.png"
    prompt = "What is the name of the product?"
    response = generate_response(image_path, prompt)
    print(f"Question: {prompt}")
    print(f"Response: {response}")