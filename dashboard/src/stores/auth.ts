import { writable } from 'svelte/store';

const storedAuth = localStorage.getItem('authToken');
export const isAuthenticated = writable(!!storedAuth);

export const auth = {
  login: (token: string) => {
    localStorage.setItem('authToken', token);
    isAuthenticated.set(true);
  },
  logout: () => {
    localStorage.removeItem('authToken');
    isAuthenticated.set(false);
  }
};
