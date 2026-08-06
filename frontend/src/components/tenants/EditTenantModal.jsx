import { useEffect, useState } from "react";

import { updateTenant } from "../../api/tenantApi";

function EditTenantModal({
    tenant,
    show,
    onClose,
    onSuccess,
}) {

    const [form, setForm] = useState({
        name: "",
        email: "",
        phone: "",
        description: "",
        support_email: "",
        sender_name: "",
        reply_to_email: "",
        is_active: true,
    });

    useEffect(() => {

        if (tenant) {

            setForm({
                name: tenant.name,
                email: tenant.email,
                phone: tenant.phone || "",
                description: tenant.description || "",

                support_email: tenant.support_email || "",
                sender_name: tenant.sender_name || "",
                reply_to_email: tenant.reply_to_email || "",

                is_active: tenant.is_active,
            });

        }

    }, [tenant]);

        if (!show || !tenant){
            return null;
        } 

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

            await updateTenant(
                tenant.uuid,
                form
            );

            onSuccess();


        } catch (error) {

            console.log(error.response?.data);

        }

    };

    if (!tenant) return null;

    return (

        <div
            className="modal d-block"
            tabIndex="-1"
            style={{ backgroundColor: "rgba(0,0,0,0.5)" }}
        >

            <div className="modal-dialog">

                <div className="modal-content">

                    <form onSubmit={handleSubmit}>

                        <div className="modal-header">

                            <h5>Edit Tenant</h5>

                            <button
                                type="button"
                                className="btn-close"
                                onClick={onClose}
                            />

                        </div>

                        <div className="modal-body">

                            <div className="mb-3">

                                <label>Name</label>

                                <input
                                    className="form-control"
                                    name="name"
                                    value={form.name}
                                    onChange={handleChange}
                                />

                            </div>

                            <div className="mb-3">

                                <label>Email</label>

                                <input
                                    className="form-control"
                                    name="email"
                                    value={form.email}
                                    onChange={handleChange}
                                />

                            </div>

                            <div className="mb-3">

                                <label>Phone</label>

                                <input
                                    className="form-control"
                                    name="phone"
                                    value={form.phone}
                                    onChange={handleChange}
                                />

                            </div>

                            <div className="mb-3">

                                <label>Description</label>

                                <textarea
                                    className="form-control"
                                    rows="3"
                                    name="description"
                                    value={form.description}
                                    onChange={handleChange}
                                />

                            </div>

                            <div className="mb-3">
                                <label>Support Mail</label>

                                <input
                                    type="email"
                                    className="form-control"
                                    name="support_email"
                                    value={form.support_email}
                                    onChange={handleChange}
                                />
                            </div>

                            <div className="mb-3">
                                <label>Sender Name</label>

                                <input
                                    className="form-control"
                                    name="sender_name"
                                    value={form.sender_name}
                                    onChange={handleChange}
                                />
                            </div>

                            <div className="mb-3">
                                <label>Reply-To Mail</label>

                                <input
                                    type="email"
                                    className="form-control"
                                    name="reply_to_email"
                                    value={form.reply_to_email}
                                    onChange={handleChange}
                                />
                            </div>

                            <div className="form-check">

                                <input
                                    type="checkbox"
                                    className="form-check-input"
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
                                className="btn btn-primary"
                                type="submit"
                            >
                                Save Changes
                            </button>

                        </div>

                    </form>

                </div>

            </div>

        </div>

    );

}

export default EditTenantModal;