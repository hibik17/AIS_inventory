import { memo, VFC } from "react";

export const RecommendTitle: VFC = memo(() => {
  return (
    <div className="w-full">
      <p className="text-right pt-16 mr-64 text-white text-6xl font-thin italic">
        Today's News
        <br />
        ×
        <br />
        Recommended Books
      </p>
    </div>
  );
});
