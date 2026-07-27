import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

function Navbar() {

    const { logout } = useAuth();

    const navigate = useNavigate();

    const handleLogout = () => {

        logout();

        navigate("/login");

    };

    return (

        <nav className="navbar navbar-light bg-white border-bottom px-4">

            <h4 className="mb-0">
                Admin Panel
            </h4>

            <button
                className="btn btn-outline-danger"
                onClick={handleLogout}
            >
                <i className="bi bi-box-arrow-right me-2"></i>

                Logout
            </button>

        </nav>

    );

}

export default Navbar;