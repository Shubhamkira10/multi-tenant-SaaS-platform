import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function ProtectedRoute({ children, allowedRoles = [] }) {
    const { accessToken, userType } = useAuth();
    const location = useLocation();

    // Not Logged In
    if (!accessToken) {
        return <Navigate to="/login" replace state={{ from: location }} />;
    }

    // Role Check
    if (
        allowedRoles.length > 0 &&
        !allowedRoles.includes(userType)
    ) {
        return <Navigate to="/login" replace />;
    }

    return children;
}

export default ProtectedRoute;