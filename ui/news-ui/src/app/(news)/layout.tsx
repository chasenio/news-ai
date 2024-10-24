import {ReactChildren} from "@/types/page";

export default async function Layout({children}: ReactChildren) {

  return (
      <>
        <main className="mx-auto min-h-80 grid w-full max-w-6xl gap-2">
          {children}
        </main>
      </>
  )
}