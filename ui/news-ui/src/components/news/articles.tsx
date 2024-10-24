'use client'

import {FC} from "react"
import {articleStore} from "@/store/article"
import {useEffect} from "react";

import {Article} from "@/store/article";

type ArticleItemProps = {
  article: Article
}

// 将时间显示为 xx ago
const timeAgo = (time: string) => {
  const date = new Date(time)
  // get utc time now
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const seconds = diff / 1000
  if (seconds < 60) {
    return `${Math.floor(seconds)} s ago`
  }

  const minutes = seconds / 60
  if (minutes < 60) {
    return `${Math.floor(minutes)} m ago`
  }

  const hours = minutes / 60
  if (hours < 24) {
    return `${Math.floor(hours)} h ago`
  }

  const days = hours / 24
  return `${Math.floor(days)} d ago`
}


// News 显示的样式
const ArticleItem: FC<ArticleItemProps> = ({article}) => {
  return (
      <div className={"flex w-full rounded-md h-25 items-center justify-center gap-2 hover:bg-gray-200 p-1"}>
        <div className={"shrink-0 w-[50px] text-muted-foreground text-sm text-nowrap"}>
          {timeAgo(article.publishedAt)}
        </div>
        <div className={"shrink w-full text-md ml-3 font-mono sm:text-lg"}>
          <a href={article.articleUrl} target="_blank" rel="noreferrer">
            {article.title}
          </a>
        </div>
        <div className={"flex-none w-27 text-sm"}>
          <span>
          {article.source}
          </span>
        </div>
      </div>
  )
}


export const Articles = () => {
  const getArticles = articleStore(state => state.getArticles)
  const articles = articleStore(state => state.articles)

  useEffect(() => {
    getArticles(1, 10)
  }, [getArticles]);

  return (
      <div className={"flex flex-col w-full gap-3 p-2"}>
        {
          articles.map((article: Article) => {
            return (
                <ArticleItem key={article.articleId} article={article}/>
            )
          })
        }
      </div>
  )
}
