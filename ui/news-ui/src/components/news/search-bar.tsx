'use client'

import {Input} from "@/components/ui/input";
import {SearchIcon} from "lucide-react";
import {articleStore} from "@/store/article";

export const SearchBar = () => {

  const getArticle = articleStore((state) => state.getArticles)
  const query = articleStore((state) => state.query)
  const setQuery = articleStore((state) => state.setQuery)

  return (
      <div className="flex w-full items-center gap-x-6 px-1 py-2">
        <div className={"relative h-12 flex-1 "}>
          <Input placeholder={"Search News"} className={"flex h-full w-full ps-10"} onChange={(e) => {
            setQuery(e.target.value)
            getArticle(1, 10, e.target.value)
          }}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && query) {
              getArticle(1, 10, query)
            }
          }}
          />
          <SearchIcon className={"absolute left-4 top-[50%] h-5 w-5 translate-y-[-50%] text-muted-foreground"}/>
        </div>
      </div>
  )
}
