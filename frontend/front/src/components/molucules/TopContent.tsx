import { memo, VFC } from "react";

import TopImage from "../Image/TopImage.png";
import { TopTitle } from "../atom/TopTitle";

export const TopContent: VFC = memo(() => {
  return (
    <div className="flex">
      <div className="w-7/12">
        <img
          src={TopImage}
          alt="topimage"
          className="object-fit animate-fade-in-up w-full"
        />
      </div>
      <div className="inline w-5/12">
        <TopTitle />
        <p className="text-2xl text-left pt-16 text-blue-500 animate-fade-in-up">
          This is the site that you can find your new book to read. which is
          releted to today’s news by useing machine learning.
        </p>
        <p className="text-2xl text-left pt-8 text-blue-500 animate-fade-in-up">
          have fan to find your new book!
        </p>
      </div>
    </div>
  );
});
