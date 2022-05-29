from newspaper import Article
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=['POST'])
def resolve_and_summarize():
    article_url = request.json['article_url']
    article = Article(article_url)
    try:
        article.download()
        article.parse()
        article.nlp()
        output_value = article.summary

    except Exception as e:
        output_value = "Error: " + repr(e)
        print(repr(e))
    
    finally:
        return output_value