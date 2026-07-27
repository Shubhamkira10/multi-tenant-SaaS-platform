import { useState } from "react";
import { createAgent } from "../../api/userApi";

function AddAgentModal({ show, onClose, onSuccess }) {

    const [form, setForm] = useState({
        first_name: "",
        last_name: "",
        email: "",
        password: "",
    });

    const [loading, setLoading] = useState(false);

    if (!show) return null;

    const handleChange = (e) => {

        setForm({
            ...form,
            [e.target.name]: e.target.value,
        });

    };

    const handleSubmit = async (e) => {

        e.preventDefault();

        try {

            setLoading(true);

            await createAgent({
                ...form,
                role: "agent",
            });

            setForm({
                first_name: "",
                last_name: "",
                email: "",
                password: "",
            });

            onSuccess();

        }

        catch (error) {

            console.error(error);

            alert(
                error?.response?.data?.message ||
                "Unable to create agent."
            );

        }

        finally {

            setLoading(false);

        }

    };

    return (

        <div
            className="modal fade show d-block"
            style={{ backgroundColor: "rgba(0,0,0,0.5)" }}
        >

            <div className="modal-dialog">

                <div className="modal-content">

                    <div className="modal-header">

                        <h5 className="modal-title">

                            Add Agent

                        </h5>

                        <button
                            className="btn-close"
                            onClick={onClose}
                        ></button>

                    </div>

                    <form onSubmit={handleSubmit}>

                        <div className="modal-body">

                            <div className="mb-3">

                                <label className="form-label">
                                    First Name
                                </label>

                                <input
                                    type="text"
                                    name="first_name"
                                    className="form-control"
                                    value={form.first_name}
                                    onChange={handleChange}
                                    required
                                />

                            </div>

                            <div className="mb-3">

                                <label className="form-label">
                                    Last Name
                                </label>

                                <input
                                    type="text"
                                    name="last_name"
                                    className="form-control"
                                    value={form.last_name}
                                    onChange={handleChange}
                                    required
                                />

                            </div>

                            <div className="mb-3">

                                <label className="form-label">
                                    Email
                                </label>

                                <input
                                    type="email"
                                    name="email"
                                    className="form-control"
                                    value={form.email}
                                    onChange={handleChange}
                                    required
                                />

                            </div>

                            <div className="mb-3">

                                <label className="form-label">
                                    Password
                                </label>

                                <input
                                    type="password"
                                    name="password"
                                    className="form-control"
                                    value={form.password}
                                    onChange={handleChange}
                                    required
                                />

                            </div>

                        </div>

                        <div className="modal-footer">

                            <button
                                type="button"
                                className="btn btn-secondary"
                                onClick={onClose}
                            >
                                Cancel
                            </button>

                            <button
                                type="submit"
                                className="btn btn-primary"
                                disabled={loading}
                            >
                                {loading ? "Saving..." : "Create Agent"}
                            </button>

                        </div>

                    </form>

                </div>

            </div>

        </div>

    );

}

export default AddAgentModal;