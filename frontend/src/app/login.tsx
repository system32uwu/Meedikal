import React, { FormEvent, useState } from "react";
import { useHistory } from "react-router-dom";

interface IProps {}

export const Login: React.FC<IProps> = ({}) => {
  const [ci, setCi] = useState<any>("");
  const [password, setPassword] = useState<any>("");
  const { push } = useHistory();

  const handleLogin = (event: FormEvent) => {
    event.preventDefault();
    fetch("http://localhost:5000/api/auth/login", {
      method: "POST",
      body: JSON.stringify({ ci: ci, password: password }),
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((data) => {
        console.log(data);
        push("/app/dashboard");
      })
      .catch((e) => console.log(e));
  };
  return (
    <div>
      <form onSubmit={handleLogin}>
        <label htmlFor="ci">CI: </label>
        <input
          type="text"
          name="ci"
          value={ci}
          onChange={(event: FormEvent<HTMLInputElement>) =>
            setCi(event.currentTarget.value)
          }
        />
        <label htmlFor="password">Password: </label>
        <input
          type="text"
          name="password"
          value={password}
          onChange={(event: FormEvent<HTMLInputElement>) =>
            setPassword(event.currentTarget.value)
          }
        />
        <input type="submit" value="login" />
      </form>
    </div>
  );
};
