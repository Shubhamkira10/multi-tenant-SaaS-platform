import { createContext, useContext, useState } from "react";

const AuthContext = createContext();

export function AuthProvider({ children }) {
    const [accessToken, setAccessToken] = useState(
        localStorage.getItem("access_token")
    );

    const [userType, setUserType] = useState(
        localStorage.getItem("user_type")
    );

    const login = (token, type, features = []) => {

        localStorage.setItem("access_token", token);
        localStorage.setItem("user_type", type);
        localStorage.setItem("features", JSON.stringify(features));

        setAccessToken(token);
        setUserType(type);
        setFeatures(features);
    };

    const logout = () => {

        localStorage.removeItem("access_token");
        localStorage.removeItem("user_type");
        localStorage.removeItem("features");

        setAccessToken(null);
        setUserType(null);
        setFeatures([]);
    };

    const [features, setFeatures] = useState(() => {
        const saved = localStorage.getItem("features");
        return saved ? JSON.parse(saved) : [];
    });

    return (
        <AuthContext.Provider
            value={{
                accessToken,
                userType,
                features,
                setFeatures,
                login,
                logout,
                isAuthenticated: !!accessToken,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
}

export const useAuth = () => useContext(AuthContext);