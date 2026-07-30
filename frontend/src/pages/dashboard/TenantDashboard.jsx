import { useEffect, useRef, useState } from "react";

import TenantLayout from "../../layouts/TenantLayout";
import {
    uploadTenantData,
    getCurrentTenant,
} from "../../api/tenantApi";

function TenantDashboard() {

    const fileInput = useRef(null);
    const [tenant, setTenant] = useState(null);
    const handleUpload = async (e) => {
        const file = e.target.files[0];

        if (!file) return;
        try {
            await uploadTenantData(file);
            alert("Company data uploaded successfully.");

        } catch (error) {
            console.error("Upload Error:", error);

            if (error.message) {
                alert(error.message);
            } else {
                alert("Upload failed.");
            }
        }

    };

    useEffect(() => {
        const loadTenant = async () => {
            try {
                const response = await getCurrentTenant();
                setTenant(response.data);
            } catch (err) {
                console.error(err);
            }
        };

        loadTenant();
    }, []);

    return (

        <TenantLayout>

            <div className="container-fluid">

                <div className="mb-4 d-flex justify-content-between align-items-center">

                    <div>

                        <h2>Tenant Dashboard</h2>

                        <p className="text-muted mb-0">
                            Welcome to the Tenant Management Panel
                        </p>

                    </div>

                    <div className="d-flex flex-column align-items-end">

                        <button
                            className="btn btn-primary"
                            onClick={() => fileInput.current.click()}
                        >
                            <i className="bi bi-upload me-2"></i>
                            Upload Company Data
                        </button>

                        <small className="text-muted mt-2">
                            <strong>Company UUID:</strong> {tenant?.uuid}
                        </small>

                        <input
                            ref={fileInput}
                            type="file"
                            hidden
                            accept=".zip"
                            onChange={handleUpload}
                        />

                    </div>

                </div>

                <div className="row g-4">

                    <div className="col-md-4">

                        <div className="card shadow-sm">

                            <div className="card-body">

                                <h6>Total Agents</h6>

                                <h2>0</h2>

                            </div>

                        </div>

                    </div>

                    <div className="col-md-4">

                        <div className="card shadow-sm">

                            <div className="card-body">

                                <h6>Total Users</h6>

                                <h2>0</h2>

                            </div>

                        </div>

                    </div>

                    <div className="col-md-4">

                        <div className="card shadow-sm">

                            <div className="card-body">

                                <h6>Total Interns</h6>

                                <h2>0</h2>

                            </div>

                        </div>

                    </div>

                </div>

            </div>

        </TenantLayout>

    );

}

export default TenantDashboard;