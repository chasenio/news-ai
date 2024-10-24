'use client'

import {
  Card,
  CardHeader,
  CardTitle,
  CardContent
} from "@/components/ui/card"

import ReactMarkdown from 'react-markdown';
import gfm from 'remark-gfm';
import {Spinner} from "flowbite-react";

import {summaryStore} from "@/store/ai";
import {Button} from "@/components/ui/button";


export const Summary = () => {
  const getSummary = summaryStore(state => state.getSummary)
  const summary = summaryStore(state => state.summary)
  const loading = summaryStore(state => state.loading)

  return (
      <div className="flex flex-col items-center justify-center">
        <div className="w-full p-2 pb-3 gap-2 leading-normal tracking-wide">
          {
              !!summary && (
                  <Card className={"p-6"}>
                    <CardHeader className={"pl-0 pt-2 pb-3 text-2xl"}>
                      <CardTitle>Summary</CardTitle>
                    </CardHeader>
                    <CardContent className={"p-1"}>
                      <ReactMarkdown remarkPlugins={[gfm]}>
                        {summary}
                      </ReactMarkdown>
                    </CardContent>
                  </Card>
              )

          }
        </div>
        <Button onClick={getSummary}>
          {
              loading && <Spinner size={"md"} className={"p-1 m-2"}/>
          }
          {"What's happen?"}
        </Button>
      </div>
  );
}