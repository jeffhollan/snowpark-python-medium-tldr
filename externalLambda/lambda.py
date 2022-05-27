import os
import openai
import json



def handler(event, context):
    event_body = {}

    openai.api_key = os.getenv("OPENAI_API_KEY")

    status_code = 200
    array_of_rows_to_return = []

    try:
        event_body = event["body"]

        payload = json.loads(event_body)
        rows = payload["data"]

        for row in rows:
            row_number = row[0]

            text = row[1]

            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=text + "\n\ntl;dr\n\n",
                temperature=0.7,
                max_tokens=60,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
                )
            
            output_value = response.choices[0].text

            row_to_return = [row_number, output_value]

            array_of_rows_to_return.append(row_to_return)

        json_compatible_string_to_return = json.dumps({"data" : array_of_rows_to_return})

    except Exception as err:
        status_code = 400
        json_compatible_string_to_return = event_body

    return {
        'statusCode': status_code,
        'body': json_compatible_string_to_return
    }