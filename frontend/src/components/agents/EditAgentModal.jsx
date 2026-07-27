import { useEffect, useState } from "react";
import { updateUser } from "../../api/userApi";

function EditAgentModal({
    show,
    agent,
    onClose,
    onSuccess,
}) {

    const [form, setForm] = useState({
        first_name: "",
        last_name: "",
        email: "",
        is_active: true,
    });

    const [loading, setLoading] = useState(false);

    useEffect(() => {

        if (agent) {

            setForm({
                first_name: agent.first_name || "",
                last_name: agent.last_name || "",
                email: agent.email || "",
                is_active: agent.is_active,
            });

        }

    }, [agent]);

    if (!show || !agent) return null;

    const handleChange = (e) => {

        const { name, value, type, checked } = e.target;

        setForm({
            ...form,
            [name]: type === "checkbox" ? checked : value,
        });

    };

    const handleSubmit = async (e) => {

        e.preventDefault();

        try {

            setLoading(true);

            await updateUser(agent.uuid, form);

            onSuccess();

        }

        catch (error) {

            console.error(error);

            alert(
                error?.response?.data?.message ||
                "Unable to update agent."
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
                            Edit Agent
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
                                    className="form-control"
                                    name="first_name"
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
                                    className="form-control"
                                    name="last_name"
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
                                    className="form-control"
                                    name="email"
                                    value={form.email}
                                    onChange={handleChange}
                                    required
                                />

                            </div>

                            <div className="form-check">

                                <input
                                    className="form-check-input"
                                    type="checkbox"
                                    name="is_active"
                                    checked={form.is_active}
                                    onChange={handleChange}
                                />

                                <label className="form-check-label">
                                    Active
                                </label>

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
                                className="btn btn-warning"
                                disabled={loading}
                            >
                                {loading ? "Updating..." : "Update Agent"}
                            </button>

                        </div>

                    </form>

                </div>

            </div>

        </div>

    );

}

export default EditAgentModal;