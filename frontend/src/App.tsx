import React from "react";
import MeedikalLanding from "./meedikalLanding";
import MeedikalApp from "./meedikalApp";
import { Route, Switch, BrowserRouter } from "react-router-dom";
import { NotFound } from "./components/notFound";

interface IProps {}

const App: React.FC<IProps> = () => {
  return (
    <BrowserRouter>
      <Switch>
        <Route path="/app">
          <MeedikalApp />
        </Route>
        <Route path="/">
          <MeedikalLanding />
        </Route>
        <Route component={NotFound} />
      </Switch>
    </BrowserRouter>
  );
};

export default App;
