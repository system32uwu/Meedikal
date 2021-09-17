import React from "react";
import { RouteComponentProps } from "@reach/router";
interface IProps extends RouteComponentProps {}

export const Home: React.FC<IProps> = () => {
  return <div>landing home page.</div>;
};
