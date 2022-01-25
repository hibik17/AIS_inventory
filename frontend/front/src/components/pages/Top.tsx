import { VFC, memo } from "react";
import { TopContent } from "../molucules/TopContent";

import { Header } from "../templates/Header";

export const Top: VFC = memo(() => {
  return (
    <div className="h-full w-full bg-gray-300">
      <Header
        recommendStyle="text-blue-500"
        infoStyle="text-blue-500"
        isTop={true}
      />
      <TopContent />
    </div>
  );
});
