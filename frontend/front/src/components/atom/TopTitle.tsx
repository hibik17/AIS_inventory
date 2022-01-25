import { memo, VFC } from "react";

export const TopTitle: VFC = memo(() => {
  return (
    <p className="text-8xl italic text-center pr-16 pt-32 font-bold text-blue-500 animate-fade-in-up">
      AI × Library
    </p>
  );
});
