import HyperText from "@/components/ui/hyper-text";

export function FinanceNews() {
  return (
      <div className={"container flex flex-col items-center justify-center py-10 gap-10 space-y-14"}>
        <HyperText
            className="text-4xl font-bold text-black dark:text-white"
            text="Finances News"
        />
      </div>
  );
}
