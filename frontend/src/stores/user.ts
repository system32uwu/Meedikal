import create, { State } from "zustand";
import { get } from "../util/request";
import { User } from "../types";

interface userState extends State {
  user: User | null;
  fetch: () => Promise<User | null | undefined>;
}

export const useUserStore = create<userState>((set, _get) => ({
  user: null,
  fetch: async () => {
    if (!_get().user) {
      return await get<User>("http://localhost:5000/api/auth/me")
        .then((data) => {
          set((_) => ({ user: data.result }));
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
