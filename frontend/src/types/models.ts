export type ErrorResponseShape = {
  error: string;
  extraMessage: string | null;
};

export type OKResponseShape<T> = {
  result: T;
};

export interface User {
  ci: number;
  name1: string;
  surname1: string;
  sex: string;
  birthdate: Date;
  location: string;
  email: string;
  password: string;
  name2: string | null;
  surname2: string | null;
  genre: string | null;
  active: boolean | null;
  photoUrl: string | null;
}

export interface FullUser{
  user: User;
  roles: string[];
  phoneNumbers: string[];
}

export interface Auth{
  authToken: string;
}