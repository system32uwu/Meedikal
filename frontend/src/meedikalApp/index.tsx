import React, { useEffect } from "react";
import { useHistory } from "react-router-dom";
import { Dashboard } from "../components/dashboard";
import { useUserStore } from "../stores/user";

interface IProps {}

const MeedikalApp: React.FC<IProps> = () => {
  const { fetch, setCurrentRole } = useUserStore();
  const { replace } = useHistory();

  useEffect(() => {
    fetch()
      .then((_user) => {
        setCurrentRole(_user?.roles[0]); // set the first role found by default
      })
      .catch(() => replace("/login"));
  }, [fetch, replace, setCurrentRole]);

  return <Dashboard />;
};

export default MeedikalApp;

// TODO: create the dashboard skeleton and use the pulse animation alongside spinners while loading is true.
