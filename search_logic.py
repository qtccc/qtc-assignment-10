import torch
import torch.nn.functional as F
from open_clip import create_model_and_transforms, tokenizer
import pandas as pd
from PIL import Image

# Load CLIP model and preprocessing transforms
model, preprocess, _ = create_model_and_transforms('ViT-B/32', pretrained='openai')
model.eval()

# Load precomputed embeddings
df = pd.read_pickle('image_embeddings.pickle')

def encode_image_query(image_path):
    image = preprocess(Image.open(image_path)).unsqueeze(0)
    return F.normalize(model.encode_image(image), dim=-1)

def encode_text_query(text_query):
    tokenized_text = tokenizer([text_query])
    return F.normalize(model.encode_text(tokenized_text), dim=-1)

def perform_search(query_type, text_query=None, image_query=None, hybrid_weight=0.8):
    if query_type == "image-query":
        query_embedding = encode_image_query(image_query)
    elif query_type == "text-query":
        query_embedding = encode_text_query(text_query)
    elif query_type == "hybrid-query":
        text_embedding = encode_text_query(text_query)
        image_embedding = encode_image_query(image_query)
        query_embedding = F.normalize(hybrid_weight * text_embedding + (1 - hybrid_weight) * image_embedding, dim=-1)
    else:
        raise ValueError("Invalid query type")

    similarities = []
    for embedding in df['embedding']:
        embedding_tensor = torch.tensor(embedding).unsqueeze(0)
        similarity = F.cosine_similarity(query_embedding, embedding_tensor).item()
        similarities.append(similarity)
    df['similarity'] = similarities

    top_results = df.sort_values(by="similarity", ascending=False).head(10)
    return [{"image": f"/static/coco_images_resized/{row['file_name']}", "similarity": row["similarity"]} for _, row in top_results.iterrows()]

# # Text Query Example
# text_query = "A cat sitting on a sofa"
# results = perform_search("text-query", text_query=text_query)
# print(results)

# # Image Query Example
# image_query_path = "house.jpg"  # Replace with the path to your image
# results = perform_search("image-query", image_query=image_query_path)
# print(results)

# # Hybrid Query Example
# hybrid_weight = 0.8
# results = perform_search("hybrid-query", text_query=text_query, image_query=image_query_path, hybrid_weight=hybrid_weight)
# print(results)

