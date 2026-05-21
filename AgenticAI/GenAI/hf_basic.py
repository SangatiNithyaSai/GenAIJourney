from transformers import pipeline

pipe=pipeline("image-text-to-text",model="google/gemma-4-26B-A4B-it")


messages=[
    {"role":"user",
    "content":[
        {"type":"image","url":"https://huggingface.co/datasets/huggingface/documentation-images?image-viewer=7E4E42EDA0F7ED7337D3A897EB8F7762B35C8EDA"},
        {"type":"text","content":"What do see in the image?"}

    ]
    }
]

pipe(text=messages)