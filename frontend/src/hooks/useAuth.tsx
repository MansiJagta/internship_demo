import { createContext, useContext, useEffect, useMemo, useState } from "react";
import { fetchMe, login, setAuthToken, signup, type AuthUser, type UserRole } from "@/lib/api";

const TOKEN_KEY = "autovibe_token";

interface AuthContextValue {
  user: AuthUser | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  loginUser: (body: { email: string; password: string }) => Promise<void>;
  signupUser: (body: { name: string; email: string; password: string; role: UserRole }) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [token, setToken] = useState<string | null>(localStorage.getItem(TOKEN_KEY));
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const bootstrapAuth = async () => {
      if (!token) {
        setAuthToken(null);
        setIsLoading(false);
        return;
      }

      try {
        setAuthToken(token);
        const me = await fetchMe();
        setUser(me);
      } catch {
        localStorage.removeItem(TOKEN_KEY);
        setAuthToken(null);
        setToken(null);
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    };

    bootstrapAuth();
  }, [token]);

  const loginUser = async (body: { email: string; password: string }) => {
    const response = await login(body);
    localStorage.setItem(TOKEN_KEY, response.access_token);
    setAuthToken(response.access_token);
    setToken(response.access_token);
    setUser(response.user);
  };

  const signupUser = async (body: { name: string; email: string; password: string; role: UserRole }) => {
    const response = await signup(body);
    localStorage.setItem(TOKEN_KEY, response.access_token);
    setAuthToken(response.access_token);
    setToken(response.access_token);
    setUser(response.user);
  };

  const logout = () => {
    localStorage.removeItem(TOKEN_KEY);
    setAuthToken(null);
    setToken(null);
    setUser(null);
  };

  const value = useMemo(
    () => ({
      user,
      token,
      isAuthenticated: Boolean(user && token),
      isLoading,
      loginUser,
      signupUser,
      logout,
    }),
    [isLoading, token, user],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
}
