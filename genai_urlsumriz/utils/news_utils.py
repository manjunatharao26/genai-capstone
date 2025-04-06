from newspaper import Article

def get_news_article_text(url: str) -> str:
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        return f"[Error fetching article: {e}]"