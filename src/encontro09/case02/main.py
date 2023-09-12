from fastapi import FastAPI, UploadFile, File
import boto3

app = FastAPI()

# Configuração do cliente S3
s3 = boto3.client(
    's3',
    aws_access_key_id='teste',
    aws_secret_access_key='teste2',
    region_name='us-east-1'
)
bucket_name = 'meu-bucket-inteli'

@app.post("/upload/")
async def upload_file(file: UploadFile):
    # Faz o upload do arquivo para o S3
    s3.upload_fileobj(file.file, bucket_name, file.filename)
    return {"message": "Arquivo enviado com sucesso"}

@app.get("/download/{file_name}")
async def download_file(file_name: str):
    try:
        # Faz o download do arquivo do S3
        response = s3.get_object(Bucket=bucket_name, Key=file_name)
        data = response['Body'].read()
        return {"file_data": data.decode('utf-8')}
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/list/")
async def list_objects():
    try:
        # Lista todos os objetos no bucket
        response = s3.list_objects(Bucket=bucket_name)
        objects = [obj['Key'] for obj in response.get('Contents', [])]
        return {"objects": objects}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
