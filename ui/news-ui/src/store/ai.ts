import {create} from "zustand";

interface SummaryStore {
  loading: boolean
  summary: string
  getSummary: () => void
}


export const summaryStore = create<SummaryStore>((set) => ({
  loading: false,
  summary: '',
  getSummary: async () => {
    try {
      set({loading: true})
      const response = await fetch(`${process.env.NEXT_PUBLIC_API}/news/ai`, {
        method: "POST"
      })
      if (!response.ok) {
        console.log(`error ${response}`)
      }

      if (response.body === null) {
        return
      }

      // receive a response body as a stream
      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');
      let result = '';

      while (true) {
        const {done, value} = await reader.read();
        if (done) break; // 结束流

        // 解码并更新结果
        result += decoder.decode(value, {stream: true});
        set({summary: result})
      }
    } catch (error) {
      console.error(error)
    } finally {
      set({loading: false})
    }
  },
}))