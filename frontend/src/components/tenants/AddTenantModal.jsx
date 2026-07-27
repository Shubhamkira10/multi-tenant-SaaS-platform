import { useEffect, useState } from "react";
import { createTenant } from "../../api/tenantApi";
import { getFeatures } from "../../api/featureApi";

function AddTenantModal({
    show,
    onClose,
    onSuccess,
}) {

    const [form, setForm] = useState({
        name: "",
        email: "",
        password: "",
        phone: "",
        description: "",
        feature_uuids: [],
    });

    const [features, setFeatures] = useState([]);

    useEffect(() => {

        if (show) {
            loadFeatures();
        }

    }, [show]);

    const loadFeatures = async () => {

        try {

            const response = await getFeatures();
            setFeatures(response.data);

        } catch (error) {

            console.log(error);

        }

    };

    const handleChange = (e) => {

        setForm((prev) => ({
            ...prev,
            [e.target.name]: e.target.value,
        }));

    };

    const handleFeatureChange = (uuid) => {

        setForm((prev) => {

            const exists = prev.feature_uuids.includes(uuid);

            return {
                ...prev,
                feature_uuids: exists
                    ? prev.feature_uuids.filter((id) => id !== uuid)
                    : [...prev.feature_uuids, uuid],
            };

        });

    };

    const resetForm = () => {

        setForm({
            name: "",
            email: "",
            password: "",
            phone: "",
            description: "",
            feature_uuids: [],
        });

    };

    const handleSubmit = async (e) => {

        e.preventDefault();

        try {

            await createTenant(form);

            resetForm();

            onSuccess();
            onClose();

        } catch (error) {

            console.log(error.response?.data || error);

        }

    };

    if (!show) return null;

    return (

        <div
            className="modal d-block"
            tabIndex="-1"
            style={{ backgroundColor: "rgba(0,0,0,0.5)" }}
        >

            <div className="modal-dialog modal-lg">

                <div className="modal-content">

                    <form onSubmit={handleSubmit}>

                        <div className="modal-header">

                            <h5 className="modal-title">
                                Add Tenant
                            </h5>

                            <button
                                type="button"
                                className="btn-close"
                                onClick={onClose}
                            ></button>

                        </div>

                        <div className="modal-body">

                            <div className="mb-3">

                                <label className="form-label">
                                    Name
                                </label>

                                <input
                                    className="form-control"
                                    name="name"
                                    value={form.name}
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

                            <div className="mb-3">

                                <label className="form-label">
                                    Password
                                </label>

                                <input
                                    type="password"
                                    className="form-control"
                                    name="password"
                                    value={form.password}
                                    onChange={handleChange}
                                    required
                                />

                            </div>

                            <div className="mb-3">

                                <label className="form-label">
                                    Phone
                                </label>

                                <input
                                    className="form-control"
                                    name="phone"
                                    value={form.phone}
                                    onChange={handleChange}
                                />

                            </div>

                            <div className="mb-3">

                                <label className="form-label">
                                    Description
                                </label>

                                <textarea
                                    className="form-control"
                                    rows="3"
                                    name="description"
                                    value={form.description}
                                    onChange={handleChange}
                                />

                            </div>

                            <div className="mb-3">

                                <label className="form-label">
                                    Assign Features
                                </label>

                                <div
                                    className="border rounded p-3"
                                    style={{
                                        maxHeight: "220px",
                                        overflowY: "auto",
                                    }}
                                >

                                    {features.length === 0 ? (

                                        <p className="text-muted mb-0">
                                            No features available.
                                        </p>

                                    ) : (

                                        features.map((feature) => (

                                            <div
                                                key={feature.uuid}
                                                className="form-check mb-2"
                                            >

                                                <input
                                                    className="form-check-input"
                                                    type="checkbox"
                                                    id={feature.uuid}
                                                    checked={form.feature_uuids.includes(feature.uuid)}
                                                    onChange={() =>
                                                        handleFeatureChange(feature.uuid)
                                                    }
                                                />

                                                <label
                                                    className="form-check-label"
                                                    htmlFor={feature.uuid}
                                                >
                                                    {feature.name}
                                                </label>

                                            </div>

                                        ))

                                    )}

                                </div>

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
                            >
                                Create Tenant
                            </button>

                        </div>

                    </form>

                </div>

            </div>

        </div>

    );

}

export default AddTenantModal;