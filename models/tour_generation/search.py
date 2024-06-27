from annoy import AnnoyIndex
from .filter_places import data, load_data


from transformers import AutoTokenizer, AutoModel


#Mean Pooling - Take attention mask into account for correct averaging
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0] #First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
    sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    return sum_embeddings / sum_mask



#Sentences we want sentence embeddings for
sentences = ['Привет! Как твои дела?',
             'А правда, что 42 твое любимое число?']

#Load AutoModel from huggingface model repository
tokenizer = AutoTokenizer.from_pretrained("ai-forever/sbert_large_nlu_ru")
model = AutoModel.from_pretrained("ai-forever/sbert_large_nlu_ru")

def embeddings_inference(sentence):
    encoded_input = tokenizer(sentence, padding=True, truncation=True, max_length=24, return_tensors='pt')
    with torch.no_grad():
        model_output = model(**encoded_input)

    return mean_pooling(model_output, encoded_input['attention_mask'])[0]



index = AnnoyIndex(1024, 'angular')

index.load('./models/tour_generation/index.annoy')


def search(query: str):
    global index, data
    load_data()
    indexes = index.get_nns_by_vector(embeddings_inference(query), n=100)
    candidates = []
    for index_ in indexes:
        candidates.append(data.iloc[index_].to_dict())
    return candidates
