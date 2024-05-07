import json
import boto3

client = boto3.client('bedrock-runtime')

def handler(event, context):

    body = json.loads(event.get('body', '{}'))
    #setting defult prompt if none provided
    prompt = body.get('prompt', 'Write a text to be posted on my social media channels about how Amazon Bedrock works')


    model_id = "anthropic.claude-3-opus-20240229-v1:0"

    response = client.invoke_model(
                modelId=model_id,
                body=json.dumps(
{
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 1000,
    "messages": [
      {
        "role": "user",
        "content": [

          {
            "type": "text",
            "text": prompt
          }
        ]
      }
    ]
  }

                ),
            )

    # Process and print the response
    result = json.loads(response.get("body").read())
    input_tokens = result["usage"]["input_tokens"]
    output_tokens = result["usage"]["output_tokens"]
    output_list = result.get("content", [])

    print("Invocation details:")
    print(f"- The input length is {input_tokens} tokens.")
    print(f"- The output length is {output_tokens} tokens.")

    print(f"- The model returned {len(output_list)} response(s):")
    for output in output_list:
                print(output["text"])


    return {
        'statusCode': 200,
        'body': json.dumps({
            'generated-text': result
        })
    }
