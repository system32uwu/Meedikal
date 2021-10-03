import React, { useEffect, useState } from "react";
import { useHistory } from "react-router";
import { useUserStore } from "../stores/user";

interface IProps {}

const Dashboard: React.FC<IProps> = () => {
  const { user, fetch } = useUserStore();
  const [loading, setLoading] = useState<boolean>(true);
  const { replace } = useHistory();

  useEffect(() => {
    fetch()
      .then((_user) => {
        setLoading(false);
      })
      .catch(() => replace("/login"));
  }, [fetch, replace]);

  return <div>{user?.user.ci}</div>;
};

export default Dashboard;

// TODO: create the dashboard skeleton and use the pulse animation alongside spinners while loading is true.
