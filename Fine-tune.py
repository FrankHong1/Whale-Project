from openai import OpenAI
import os
import time

#client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))


def upload_data(file_path):
  with open(file_path, "rb") as file:
  #The 'with...as' syntax is necessary to ensure the file is closed properly after the block is executed
  #It's like a safer '=' command in file management context
    response = client.File.create(file = file,
                                purpose = 'fine-tune')
  data_ID = response['id']
  #OpenAI.File.create is a dictionary, and we only want the 'id' object here
  return data_ID


def fine_tune(raw_data_ID):
  response = client.FineTune.create(training_file = raw_data_ID,
                                   model = 'gpt-4o-realtime-preview')
  fine_tune_ID = response['id']
  return fine_tune_ID


def monitor(fine_tune_ID):

  while True:
    response = client.FineTune.retrieve(id = fine_tune_ID)
    status = response['status']
    print(f"Current status is: {status}")
    if status in ['succeeded', 'failed']:
      break
    time.sleep(180)

  if status == 'succeeded':
    model_ID = response['fine_tuned_model']
    print(f"The model is ready to use, the model ID is: {model_ID}")
    return model_ID

  else:
    print("Fine-tuning failed")
    return None


def training():
  data_ID = upload_data("some_data.jsonl")
  fine_tune_ID = fine_tune(data_ID)
  model_ID = monitor(fine_tune_ID)
  return model_ID


if __name__ == "__main__":
  training()