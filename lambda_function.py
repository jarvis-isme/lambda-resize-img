import json
import boto3 

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    response = s3.get_object(Bucket=bucket, Key=key)
    image_bytes = response['Body'].read()
    
    # Resize the image
    size = (200, 200)  # Define your size here
    resized_image = resize_image(image_bytes, size)
    
    # Save the resized image back to S3
    new_key = f"resized-{key}"
    s3.put_object(Bucket=bucket, Key=new_key, Body=resized_image, ContentType='image/jpeg')
    
    return {
        'statusCode': 200,
        'body': json.dumps(f"Image resized and saved as {new_key}")
    }

# resize img 
def resize_image(image_bytes, size):
    with Image.open(io.BytesIO(image_bytes)) as image:
        image = image.resize(size)
        buffer = io.BytesIO()
        image.save(buffer, 'JPEG')
        buffer.seek(0)
        return buffer