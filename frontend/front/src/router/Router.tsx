// ツールのimport
import { memo, VFC } from "react";
import { Route, Switch } from "react-router-dom";

// ページのimport
import { Top } from "../components/pages/Top";
import { Recommend } from "../components/pages/Recommend";
import { ErrorPage } from "../components/pages/ErrorPage";

export const Router: VFC = memo(() => {
  return (
    <Switch>
      <Route exact path="/">
        <Top />
      </Route>
      <Route exact path="/recommend">
        <Recommend />
      </Route>
      <Route path="*">
        <ErrorPage />
      </Route>
    </Switch>
  );
});
