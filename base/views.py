from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Dataset
from .forms import DatasetForm

# # RECOMMENDER SYSTEM CODE
import pandas as pd
import csv
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


def give_recommendations(title, cos_sim, df, id_to_index, title_to_id):
  idx = id_to_index[str(title_to_id[title])]
  if idx is None:
      print("Title Not Found")
      return None, None
  cos_sim_scores = list(enumerate(cos_sim[idx]))
  cos_sim_scores = sorted(cos_sim_scores, key=lambda x: x[1], reverse=True)
  cos_sim_scores = cos_sim_scores[:10]
  # Dataset indices
  dataset_indices = [cos_sim_score[0] for cos_sim_score in cos_sim_scores]
  similar_ids = [df.iloc[index]["id"] for index in dataset_indices]
  return similar_ids, cos_sim_scores



def anotherdataset(request, pk):
  current_dataset = Dataset.objects.get(id=pk)
  datasets = Dataset.objects.all()
  # Convert the Django QuerySet to a list of dictionaries
  data_dict = list(datasets.values())

  # Create a Pandas DataFrame from the list of dictionaries
  df = pd.DataFrame(data_dict)
  # Filling NaNs with empty string
  df["overview"] = df["overview"].fillna('')

  # Create a TFIDFVectorizer Object
  tfv = TfidfVectorizer(min_df=1, max_features=None, strip_accents="unicode", analyzer="word", token_pattern=r"\w{1,}", ngram_range=(1, 3), stop_words="english")

  # Fit the TfidfVectorizer on the "overview" text
  tfv_matrix = tfv.fit_transform(df["overview"])

  # Calculate the cosine similarity between all dataset
  cos_sim = cosine_similarity(tfv_matrix, tfv_matrix)

  # Load data from 'output.csv' and create a title-to-id mapping
  title_to_id = {}
  df.to_csv("temp.csv", index=False)
  title_to_id = {}
  with open('temp.csv', mode='r') as file:
      csv_reader = csv.DictReader(file)
      for row in csv_reader:
          title_to_id[row['title']] = row['id']
    
  id_to_index = {str(id_): index for index, id_ in enumerate(df["id"])}

  # Primary keys 
  pks, scores = give_recommendations(current_dataset.title, cos_sim, df, id_to_index, title_to_id)
  sd = []
  for pk in pks:
    dataset = Dataset.objects.get(id=pk)
    sd.append(dataset)
  return render(request, "base/anotherdataset.html", {"sd" : sd, "dataset" : current_dataset})







# -----------------------------------------------------------------



# Create your views here.
def home(request):
  datasets = Dataset.objects.all()
  return render(request, "base/home.html", {"datasets" : datasets})


def dataset(request, pk):
  dataset = Dataset.objects.get(id=pk)
  return render(request, "base/dataset.html", {"title" : dataset.title})


def upload(request):
  if request.method == "POST":
    form = DatasetForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      return redirect("home")
  else:
    form = DatasetForm()
  return render(request, "base/upload.html", {"form" : form})


def download(request, pk):
  file = Dataset.objects.get(id=pk)
  response = HttpResponse(file.file, content_type='application/force-download')
  response['Content-Disposition'] = f'attachment; filename="{file.file.name}"'
  return response