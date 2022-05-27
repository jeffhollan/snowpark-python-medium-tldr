import os
import openai
from newspaper import Article
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

            article_url = row[1]
            print("parsed url: " + article_url)
            article = Article(article_url)
            article.download()
            print("downloaded article")
            article.parse()
            print("article parsed")
            article.nlp()
            print("ran nlp")

            ### using openai to generate summary
            #
            # response = openai.Completion.create(
            #     engine="text-davinci-002",
            #     prompt=article.text + "\n\ntl;dr\n\n",
            #     temperature=0.7,
            #     max_tokens=60,
            #     top_p=1.0,
            #     frequency_penalty=0.0,
            #     presence_penalty=0.0
            #     )
            
            output_value = article.summary
            print("summary: " + output_value)

            row_to_return = [row_number, output_value]

            array_of_rows_to_return.append(row_to_return)

        json_compatible_string_to_return = json.dumps({"data" : array_of_rows_to_return})

    except Exception as err:
        status_code = 400
        json_compatible_string_to_return = [event_body, repr(err)]

    return {
        'statusCode': status_code,
        'body': json_compatible_string_to_return
    }