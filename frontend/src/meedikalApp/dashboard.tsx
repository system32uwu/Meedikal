import React, { useEffect, useState } from "react";
import { useHistory } from "react-router";
import { useUserStore } from "../stores/user";

interface IProps {}

export const Dashboard: React.FC<IProps> = () => {
  const { user, fetch } = useUserStore();
  const [loading, setLoading] = useState<boolean>(true);
  const { push } = useHistory();

  useEffect(() => {
    fetch()
      .then((_user) => {
        setLoading(false);
      })
      .catch(() => push("/app/login"));
  }, [fetch, push]);

  return <div>{user?.user.ci}</div>;
};

// TODO: create the dashboard skeleton and use the pulse animation alongside spinners while loading is true.
