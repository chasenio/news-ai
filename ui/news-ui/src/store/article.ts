import {create} from "zustand";


export type Article = {
  articleId: number
  title: string
  content: string
  source: string
  articleUrl: string
  imageUrl: string | null
  publishedAt: string
}

interface ArticleStore {
  loading: boolean
  query: string,
  articles: Array<Article>
  getArticles: (page: number, limit: number, title?: string) => void
  setArticles: (articles: Array<Article>) => void
  setQuery: (query: string) => void
}

export const articleStore = create<ArticleStore>((set) => ({
  string: '',
  loading: false,
  query: "",
  articles: [],
  getArticles: async (page: number, limit: number, title?: string) => {
    const query = new URLSearchParams(
        {
          p: page.toString(),
          limit: limit.toString(),
        }
    )
    if (title) {
      query.set("title", title)
    }

    try {
      set({loading: true})
      const response = await fetch(`${process.env.NEXT_PUBLIC_API}/news/articles?${query}`)
      if (!response.ok) {
        console.log(`error ${response}`)
      }
      const data = await response.json()
      // make article
      const articles = data.articles.map(
          (i: ArticleItemProps) => makeArticle(i)
      )

      set({articles: articles})
    } catch (err) {
      console.error(err)
    } finally {
      set({loading: false})
    }
  },
  setArticles: (articles: Array<Article>) => {
    set({articles: articles})
  },
  setQuery: (query: string) => {
    set({query})
  }
}))


interface ArticleItemProps {
  article_id: number
  title: string
  content: string
  source: string
  url: string
  image_url: string
  published_at: string
}

const makeArticle = (article: ArticleItemProps): Article => {
  return {
    articleId: article.article_id,
    title: article.title,
    content: article.content,
    source: article.source,
    articleUrl: article.url,
    imageUrl: article.image_url,
    publishedAt: article.published_at
  }
}