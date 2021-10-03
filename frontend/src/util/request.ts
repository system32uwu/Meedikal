import axios, { AxiosRequestConfig, Method } from "axios";
import { OKResponseShape, ErrorResponseShape } from "../types/index";

const serverUrl =
  process.env.NODE_ENV === "production" ? window.origin : "http://127.0.0.1:80";

export const apiUrl = `${serverUrl}/api`;

export const imagesUrl = `${serverUrl}/images`;

let _axios = axios.create({
  baseURL: apiUrl,
  headers: {
    Authorization: `Bearer ${localStorage.getItem("authToken")}`,
  },
});

export const api = () => {
  return _axios;
};

export const setApi = (config: AxiosRequestConfig) => {
  _axios = axios.create({ ...config, baseURL: apiUrl });
};

export async function apiCall<T>(
  url: string,
  method: Method,
  data?: any
): Promise<T> {
  return await api()({ url, method, data })
    .then((res) => {
      return (res.data as OKResponseShape<T>).result;
    })
    .catch((err) => {
      return Promise.reject(err.response.data as ErrorResponseShape);
    });
}
