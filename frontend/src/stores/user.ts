import create, { State } from "zustand";
import { apiCall } from "../util/request";
import { FullUser } from "../types";

interface userState extends State {
  user: FullUser | null;
  fetch: () => Promise<FullUser | null | undefined>;
}

export const useUserStore = create<userState>((set, _get) => ({
  user: null,
  fetch: async () => {
    if (!_get().user) {
      return await apiCall<FullUser>("auth/me", "POST").then((res) => {
        set((_) => ({ user: res }));
        return _get().user;
      });
    } else {
      return _get().user;
    }
  },
}));
