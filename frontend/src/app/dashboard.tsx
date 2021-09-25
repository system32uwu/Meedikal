import React, { FormEvent, useEffect, useState } from "react";
import { RouteComponentProps } from "@reach/router";

interface IProps extends RouteComponentProps {}

export const Dashboard: React.FC<IProps> = () => {
  const [photo, setPhoto] = useState<any>('');
  const [ci, setCi] = useState<any>('');
  const [password, setPassword] = useState<any>('');

  const handleChange = (event: FormEvent<HTMLInputElement>) => {
    setPhoto(event.currentTarget.value);
  };

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault()
    let formData = new FormData(document.forms.namedItem('uploadPhoto') || undefined);
        
    fetch('http://localhost:5000/api/user/photo', {
      method: "POST",
      body: formData,
      credentials: 'include'
    }).then(data => console.log(data)).catch(e => console.log(e));
  };

  const handleLogin = (event: FormEvent) => {
    event.preventDefault()
    fetch('http://localhost:5000/api/auth/login', {
      method: "POST",
      body: JSON.stringify({ ci: ci, password: password }),
      headers: {
        'Content-Type': 'application/json'
      }
    }).then(data => console.log(data)).catch(e => console.log(e));
  };

  return (
    <div>
      <form onSubmit={handleLogin}>
        <label htmlFor='ci'>CI: </label>
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
      <form onSubmit={handleSubmit} encType="multipart/form-data" method="POST" name="uploadPhoto">
        <input type="file" name="file" value={photo} onChange={handleChange} />
        <input type="submit" value="Upload" />
      </form>
    </div>
  );
};
