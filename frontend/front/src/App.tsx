import React, { memo, VFC } from "react";
import { BrowserRouter } from "react-router-dom";

import { Router } from "./router/Router";

export const App: VFC = memo(() => {
  return (
    <BrowserRouter>
      <Router />
    </BrowserRouter>
  );
});
