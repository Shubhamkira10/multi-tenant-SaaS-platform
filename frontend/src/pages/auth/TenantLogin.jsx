import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { tenantLogin } from "../../api/authApi";
import { getTenantFeatures } from "../../api/rbacApi";
import { useAuth } from "../../context/AuthContext";

function TenantLogin() {

    const navigate = useNavigate();
    const { login } = useAuth();

    const [form, setForm] = useState({
        email: "",
        password: "",
    });

    const handleChange = (e) => {

        setForm({
            ...form,
            [e.target.name]: e.target.value,
        });

    };

    const handleSubmit = async (e) => {

        e.preventDefault();

        try {

            const response = await tenantLogin(form);

            console.log(response);

            login(
                response.access_token,
                "tenant",
                response.features
            );

            navigate("/tenant/dashboard");

        } catch (error) {

            console.log(error.response?.data);

        }

    };

    return (

        <div className="container mt-5">

            <div className="row justify-content-center">

                <div className="col-md-4">

                    <div className="card shadow">

                        <div className="card-body">

                            <h3 className="text-center mb-4">

                                Tenant Login

                            </h3>

                            <form onSubmit={handleSubmit}>

                                <div className="mb-3">

                                    <label>Email</label>

                                    <input
                                        type="email"
                                        className="form-control"
                                        name="email"
                                        onChange={handleChange}
                                    />

                                </div>

                                <div className="mb-3">

                                    <label>Password</label>

                                    <input
                                        type="password"
                                        className="form-control"
                                        name="password"
                                        onChange={handleChange}
                                    />

                                </div>

                                <button
                                    className="btn btn-primary w-100"
                                >
                                    Login
                                </button>

                            </form>

                        </div>

                    </div>

                </div>

            </div>

        </div>

    );

}

export default TenantLogin;