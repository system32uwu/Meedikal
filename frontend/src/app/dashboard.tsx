import React from "react";
import { RouteComponentProps } from "@reach/router";

interface IProps extends RouteComponentProps {}

export const Dashboard: React.FC<IProps> = () => {
  return <div>this is the app dashboard</div>;
};
