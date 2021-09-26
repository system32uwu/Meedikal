import axios from "axios";
import { OKResponseShape } from "../types";

const baseUrl = "http://localhost:5000";

const apiUrl = `${baseUrl}/api`;

const imagesUrl = `${baseUrl}/images`;

const _axios = axios.create({ baseURL: apiUrl });

_axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      return Promise.reject(error.response.data);
    }
  }
);

export async function get<T>(url: string): Promise<OKResponseShape<T>> {
  return await _axios.get(url).then((res) => {
    return res.data;
  });
}
