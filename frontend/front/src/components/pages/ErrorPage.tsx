import { memo, useCallback, VFC } from "react";
import { useHistory } from "react-router-dom";

import Image from "../Image/404.png";
import Number from "../Image/4.png";
import { Button } from "../atom/Button";

export const ErrorPage: VFC = memo(() => {
  const history = useHistory();
  const BackToTop = useCallback(() => history.push("/"), [history]);
  return (
    <div
      className="h-screen 
                 bg-gradient-to-r from-gray-700 via-gray-900 to-black
                 w-full 
                 text-center 
                 animate-fade-in-up"
    >
      <div className="flex pt-32 pb-8">
        <div className="w-1/3">
          <img
            src={Number}
            alt="404image"
            className="mx-auto object-cover w-full h-full animate-pulse"
          />
        </div>
        <div className="w-1/3">
          <img
            src={Image}
            alt="404image"
            className="mx-auto object-contain w-full h-full animate-pulse"
          />
        </div>
        <div className="w-1/3">
          <img
            src={Number}
            alt="404image"
            className="mx-auto object-cover w-full h-full animate-pulse"
          />
        </div>
      </div>
      <Button RedirectPath={BackToTop}>Back to Top</Button>
    </div>
  );
});
