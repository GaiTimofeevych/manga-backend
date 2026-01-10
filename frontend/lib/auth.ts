// Ключ, под которым будем хранить токен в браузере
const TOKEN_KEY = 'manga_access_token';

export const setToken = (token: string) => {
  if (typeof window !== 'undefined') {
    localStorage.setItem(TOKEN_KEY, token);
  }
};

export const getToken = (): string | null => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem(TOKEN_KEY);
  }
  return null;
};

export const removeToken = () => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem(TOKEN_KEY);
  }
};

// Простая проверка: есть ли токен?
export const isAuthenticated = () => {
  return !!getToken();
};