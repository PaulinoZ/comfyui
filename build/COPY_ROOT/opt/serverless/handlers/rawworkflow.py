from handlers.basehandler import BaseHandler
import random
import os

"""
Handler classes are generally bound to a specific workflow file.
To modify values we have to be confident in the json structure.

One exception - RawWorkflow will send payload['workflow_json'] to the ComfyUI API after
downloading any URL's to the input directory and replacing the URL with a local path.

Any other modifications you need, such as randomising seeds should be done before submitting.
"""

class RawWorkflow(BaseHandler):
    
    WORKFLOW_JSON = None
    
    def __init__(self, payload):
        super().__init__(payload, self.WORKFLOW_JSON)
        # Store the new keys in the instance
        self.story_id = payload.get('id', False)
        self.scene_idx = payload.get('idx', False)
        self.apply_modifiers()
        # Example usage of the new keys
        print(f'Story ID: {self.story_id}, Scene Index: {self.scene_idx}')
        
        

    def apply_modifiers(self):
        print(f'INPUT DIR: {os.listdir("/opt/ComfyUI/input/")}')

        print(f'PROMPT ANTES: {self.prompt}')
        self.prompt = self.replace_urls(self.prompt)
        print(f'PROMPT INTERMEDIO: {self.prompt}')
        self.prompt["prompt"]["27"]["inputs"]["image"] = self.prompt["prompt"]["69"]["inputs"]["url"]

        self.prompt["prompt"].pop("69")

        print(f'PROMPT DESPUES: {self.prompt}')

        print(f'INPUT DIR: {os.listdir("/opt/ComfyUI/input/")}')

        self.prompt["prompt"]["3"]["inputs"]["seed"] = self.get_value(
            "seed",
            random.randint(0,2**32))

        print(f'PROMPT FINAL: {self.prompt}')

        
"""
aws_* values can alternatively be set as AWS_* environment variables
Example Request Body:

{
    "input": {
        "handler": "RawWorkflow",
        "aws_access_key_id": "your-s3-access-key",
        "aws_secret_access_key": "your-s3-secret-access-key",
        "aws_endpoint_url": "https://my-endpoint.backblaze.com",
        "aws_bucket_name": "your-bucket",
        "webhook_url": "your-webhook-url",
        "webhook_extra_params": {},
        "workflow_json": {
            "3": {
              "inputs": {
                "seed": 280823642470253,
                "steps": 20,
                "cfg": 8,
                "sampler_name": "dpmpp_2m",
                "scheduler": "normal",
                "denoise": 0.8700000000000001,
                "model": [
                  "14",
                  0
                ],
                "positive": [
                  "6",
                  0
                ],
                "negative": [
                  "7",
                  0
                ],
                "latent_image": [
                  "12",
                  0
                ]
              },
              "class_type": "KSampler"
            },
            "6": {
              "inputs": {
                "text": "photograph of victorian woman with wings, sky clouds, meadow grass",
                "clip": [
                  "14",
                  1
                ]
              },
              "class_type": "CLIPTextEncode"
            },
            "7": {
              "inputs": {
                "text": "watermark, text",
                "clip": [
                  "14",
                  1
                ]
              },
              "class_type": "CLIPTextEncode"
            },
            "8": {
              "inputs": {
                "samples": [
                  "3",
                  0
                ],
                "vae": [
                  "14",
                  2
                ]
              },
              "class_type": "VAEDecode"
            },
            "9": {
              "inputs": {
                "filename_prefix": "ComfyUI",
                "images": [
                  "8",
                  0
                ]
              },
              "class_type": "SaveImage"
            },
            "10": {
              "inputs": {
                "image": "https://raw.githubusercontent.com/comfyanonymous/ComfyUI/master/input/example.png",
                "upload": "image"
              },
              "class_type": "LoadImage"
            },
            "12": {
              "inputs": {
                "pixels": [
                  "10",
                  0
                ],
                "vae": [
                  "14",
                  2
                ]
              },
              "class_type": "VAEEncode"
            },
            "14": {
              "inputs": {
                "ckpt_name": "v1-5-pruned-emaonly.ckpt"
              },
              "class_type": "CheckpointLoaderSimple"
            }
        }
    }
}

"""
           
