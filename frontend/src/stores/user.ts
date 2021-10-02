import create, { State } from "zustand";
import { api, apiCall } from "../util/request";
import { FullUser, User } from "../types";

interface userState extends State {
  user: FullUser | null;
  fetch: () => Promise<FullUser | null | undefined>;
}

export const useUserStore = create<userState>((set, _get) => ({
  user: null,
  fetch: async () => {
    if (!_get().user) {
      return await apiCall<FullUser>(
        "http://localhost:5000/api/auth/me",
        "POST"
      )
        .then((res) => {
          set((_) => ({ user: res }));
          return _get().user;
        })
        .catch((err) => {
          console.log(err);
          return null;
        });
    } else {
      return _get().user;
    }
  },
}));
