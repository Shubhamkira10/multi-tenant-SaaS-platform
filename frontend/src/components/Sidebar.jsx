import { NavLink } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function Sidebar({ role = "platform" }) {

    const { features } = useAuth();

    return (

        <div
            className="bg-dark text-white p-3 d-flex flex-column"
            style={{
                width: "260px",
                minWidth: "260px",
                maxWidth: "260px",
                height: "100vh",
                position: "sticky",
                top: 0,
                overflowY: "auto",
                flexShrink: 0,
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

                        {features.map((feature) => (

                            <li
                                className="nav-item"
                                key={feature.uuid}
                            >

                                <NavLink
                                    to={`/tenant/${feature.route}`}
                                    className="nav-link text-white"
                                >

                                    <i className={`${feature.icon} me-2`}></i>

                                    {feature.name}

                                </NavLink>

                            </li>

                        ))}

                    </>
                )}

            </ul>

        </div>

    );

}

export default Sidebar;