import axios, { AxiosRequestConfig, Method } from "axios";
import { OKResponseShape, ErrorResponseShape } from "../types/index";
export const baseUrl = "http://localhost:5000";

export const apiUrl = `${baseUrl}/api`;

export const imagesUrl = `${baseUrl}/images`;

let _axios = axios.create({ baseURL: apiUrl });

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
