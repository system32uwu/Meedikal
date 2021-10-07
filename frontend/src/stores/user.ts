import create, { UndoState } from "zundo";
import { apiCall } from "../util/request";
import { FullUser } from "../types";
import { history } from "../App";
interface userState extends UndoState {
  user: FullUser | null | undefined;
  fetch: () => Promise<FullUser | null | undefined>;
  currentRole: string | undefined;
  setCurrentRole: (role: string | undefined) => void;
  logout: () => void;
  setUser: (user: FullUser | null | undefined) => void;
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
  currentRole: undefined,
  setCurrentRole: (role: string | undefined) =>
    set((_) => ({ currentRole: role })),
  logout: () => {
    if (process.env.NODE_ENV === "development") {
      localStorage.removeItem("authToken");
      history.push("/");
    } else {
      apiCall("/auth/logout", "POST").then(() => {
        history.push("/");
      });
    }
    set((_) => ({ user: null, currentRole: undefined }));
  },
  setUser: (user: FullUser | null | undefined) => {
    set((_) => ({ user: user }));
  },
}));
