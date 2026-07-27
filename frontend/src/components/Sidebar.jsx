import { NavLink } from "react-router-dom";

function Sidebar({ role = "platform" }) {

    return (

        <div
            className="bg-dark text-white p-3"
            style={{
                width: "250px",
                minHeight: "100vh",
            }}
        >

            <h3 className="mb-4">
                {role === "platform" ? "Platform Admin" : "Tenant Panel"}
            </h3>

            <ul className="nav flex-column">

                {role === "platform" && (
                    <>
                        <li className="nav-item">

                            <NavLink
                                to="/dashboard"
                                className="nav-link text-white"
                            >
                                <i className="bi bi-speedometer2 me-2"></i>
                                Dashboard
                            </NavLink>

                        </li>

                        <li className="nav-item">

                            <NavLink
                                to="/tenants"
                                className="nav-link text-white"
                            >
                                <i className="bi bi-buildings me-2"></i>
                                Tenants
                            </NavLink>

                        </li>

                    </>
                )}

                {role === "tenant" && (
                    <>
                        <li className="nav-item">

                            <NavLink
                                to="/tenant/dashboard"
                                className="nav-link text-white"
                            >
                                <i className="bi bi-speedometer2 me-2"></i>
                                Dashboard
                            </NavLink>

                        </li>

                        <li className="nav-item">

                            <NavLink
                                to="/agents"
                                className="nav-link text-white"
                            >
                                <i className="bi bi-person-badge me-2"></i>
                                Agents
                            </NavLink>

                        </li>

                        <li className="nav-item">

                            <NavLink
                                to="/users"
                                className="nav-link text-white"
                            >
                                <i className="bi bi-people me-2"></i>
                                Users
                            </NavLink>

                        </li>

                        <li className="nav-item">

                            <NavLink
                                to="/interns"
                                className="nav-link text-white"
                            >
                                <i className="bi bi-person-workspace me-2"></i>
                                Interns
                            </NavLink>

                        </li>

                        <li className="nav-item">

                            <NavLink
                                to="/assign-features"
                                className="nav-link text-white"
                            >
                                <i className="bi bi-grid me-2"></i>

                                Assign Features

                            </NavLink>

                        </li>

                    </>
                )}

            </ul>

        </div>

    );

}

export default Sidebar;