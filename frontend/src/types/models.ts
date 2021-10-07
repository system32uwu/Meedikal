export interface Dictionary<T> {
  [key: string]: T;
}

export type ErrorResponseShape = {
  error: string;
  extraMessage: string | null;
};

export type OKResponseShape<T> = {
  result: T;
};

export interface User{
  ci: number;
  name1: string;
  surname1: string;
  sex: string;
  birthdate: string;
  location: string;
  email: string;
  password: string;
  name2?: string | null;
  surname2?: string | null;
  genre?: string | null;
  active: boolean | null;
  photoUrl?: string | null;
  [key: string]: any;
}

export interface FullUser {
  user: User;
  roles?: string[];
  phoneNumbers?: { ci: number; phone: string }[];
  [key: string]: any;
}

export interface Auth {
  authToken: string;
}
