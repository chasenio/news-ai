

import {Metadata} from "next";

import {SearchBar} from "@/components/news/search-bar"
import {Articles} from "@/components/news/articles";
import {FinanceNews} from "@/components/news/hyper-text";
import {Summary} from "@/components/ai/summary";

export const metadata: Metadata = {
  title: "Finance News",
  description: "Finance news for the world.",
}


export default function Page() {
  return (
      <>
        <FinanceNews/>
        <Summary/>
        <SearchBar/>
        <Articles/>
      </>
  );
}
