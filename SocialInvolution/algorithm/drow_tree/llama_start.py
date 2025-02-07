from langchain.llms.base import LLM
from typing import Any, List, Optional
from langchain.callbacks.manager import CallbackManagerForLLMRun
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class LLaMA3_LLM(LLM):
    # 基于本地 llama3 自定义 LLM 类
    tokenizer: AutoTokenizer = None
    model: AutoModelForCausalLM = None
        
    def __init__(self, mode_name_or_path :str):
        super().__init__()
        print("正在从本地加载模型...")
        self.tokenizer = AutoTokenizer.from_pretrained(mode_name_or_path, use_fast=False)
        self.model = AutoModelForCausalLM.from_pretrained(mode_name_or_path, torch_dtype=torch.bfloat16, device_map="auto")
        self.tokenizer.pad_token = self.tokenizer.eos_token
        print("完成本地模型的加载")

    def build_input(self, prompt, history=[]):
        user_format='<|start_header_id|>user<|end_header_id|>\n\n{content}<|eot_id|>'
        assistant_format='<|start_header_id|>assistant<|end_header_id|>\n\n{content}<|eot_id|>'
        history.append({'role':'user','content':prompt})
        prompt_str = ''
        # 拼接历史对话
        for item in history:
            if item['role']=='user':
                prompt_str+=user_format.format(content=item['content'])
            else:
                prompt_str+=assistant_format.format(content=item['content'])
        return prompt_str
    
    def _call(self, prompt : str, stop: Optional[List[str]] = None,
                run_manager: Optional[CallbackManagerForLLMRun] = None,
                **kwargs: Any):
        input_str = self.build_input(prompt=prompt)
        input_ids = self.tokenizer.encode(input_str, add_special_tokens=False, return_tensors='pt').to(self.model.device)
        attention_mask = input_ids.ne(self.tokenizer.pad_token_id).int()  # 创建 attention mask
        outputs = self.model.generate(
            input_ids=input_ids, attention_mask=attention_mask,  # 添加 attention mask 参数
            max_new_tokens=512, do_sample=True,
            top_p=0.9, temperature=0.5, repetition_penalty=1.1, eos_token_id=self.tokenizer.eos_token_id
        )
        outputs = outputs.tolist()[0][len(input_ids[0]):]
        response = self.tokenizer.decode(outputs).strip().replace('<|eot_id|>', "").replace('<|start_header_id|>assistant<|end_header_id|>\n\n', '').strip()
        return response
        
    @property
    def _llm_type(self) -> str:
        return "LLaMA3_LLM"

# llm = LLaMA3_LLM(mode_name_or_path = "/home/syf/projects/huggingfaces/NousResearch/Meta-Llama-3-8B-Instruct")
# print(llm("你是谁"))