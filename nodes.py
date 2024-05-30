import os
import torch
import time
import folder_paths
import numpy as np
from ChatTTS import Chat
from scipy.io.wavfile import write as wavwrite

out_path = folder_paths.get_output_directory()
now_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(now_dir,"pretrained_models")
class ChatTTS:
    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {"text": ("STRING",{
                        "default":"""chat T T S 是一款强大的对话式文本转语音模型。它有中英混读和多说话人的能力。\
                                chat T T S 不仅能够生成自然流畅的语音，还能控制[laugh]笑声啊[laugh]，\
                                停顿啊[uv_break]语气词啊等副语言现象[uv_break]。这个韵律超越了许多开源模型[uv_break]。\
                                请注意，chat T T S 的使用应遵守法律和伦理准则，避免滥用的安全风险。[uv_break]'""",
                        "multiline": True,
                        "dynamicPrompts": True
                    }),
                    "if_sample_spk":("BOOLEAN",{
                        "default": True
                    }),
                    "prompt": ("STRING",{
                        "default":'[oral_2][laugh_0][break_6]',
                        "multiline": True
                    }),
                    "top_P":("FLOAT",{
                        "default":0.7,
                        "min": 0.,
                        "max":1
                    }),
                    "top_K":("INT",{
                        "default":20
                    }),
                    "temperature":("FLOAT",{
                        "default":0.3,
                        "min": 0.,
                        "max":1
                    }),
                    "refine_temperature":("FLOAT",{
                        "default":0.7,
                        "min": 0.,
                        "max":1
                    }),
                    "repetition_penalty":("FLOAT",{
                        "default":1.05,
                    }),
                    "use_decoder":("BOOLEAN",{
                        "default": False
                    }),
                    }
                }

    CATEGORY = "AIFSH_ChatTTS"
    DESCRIPTION = "hello world!"

    RETURN_TYPES = ("AUDIO",)

    OUTPUT_NODE = False

    FUNCTION = "tts"

    def tts(self, text,if_sample_spk,prompt,top_P,top_K,temperature,refine_temperature,
            repetition_penalty,use_decoder):
        chat = Chat()
        chat.load_models(source="local",local_path=model_path)

        if if_sample_spk:
            std, mean = torch.load(os.path.join(model_path,'asset','spk_stat.pt')).chunk(2)
            rand_spk = torch.randn(768) * std + mean
        
        params_infer_code = {
            'spk_emb': rand_spk if if_sample_spk else None, # add sampled speaker 
            'temperature': temperature, # using custom temperature
            'top_P': top_P, # top P decode
            'top_K': top_K, # top K decode
            'repetition_penalty': repetition_penalty
        }

        ###################################
        # For sentence level manual control.

        # use oral_(0-9), laugh_(0-2), break_(0-7) 
        # to generate special token in text to synthesize.
        params_refine_text = {
            'prompt': prompt,
            'temperature': refine_temperature, # using custom temperature
            'top_P': top_P, # top P decode
            'top_K': top_K, # top K decode
            'repetition_penalty': repetition_penalty
        } 
        text = text.replace('\n', '')
        wav = chat.infer(text, 
                         params_refine_text=params_refine_text, 
                         params_infer_code=params_infer_code,
                         use_decoder=use_decoder)
        wav_path = os.path.join(out_path,f"chattts_{time.time()}.wav")
        wavwrite(wav_path,24000,
        (np.array(wav) * 32768).astype(
            np.int16
        )) 
        return (wav_path,)

class PreViewAudio:
    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {"audio": ("AUDIO",),}
                }

    CATEGORY = "AIFSH_ChatTTS"
    DESCRIPTION = "hello world!"

    RETURN_TYPES = ()

    OUTPUT_NODE = True

    FUNCTION = "load_audio"

    def load_audio(self, audio):
        audio_name = os.path.basename(audio)
        tmp_path = os.path.dirname(audio)
        audio_root = os.path.basename(tmp_path)
        return {"ui": {"audio":[audio_name,audio_root]}}
