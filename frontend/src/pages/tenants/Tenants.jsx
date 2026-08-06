import { useEffect, useState } from "react";

import AdminLayout from "../../layouts/AdminLayout";
import { getTenants, uploadTenantData, } from "../../api/tenantApi";
import AddTenantModal from "../../components/tenants/AddTenantModal";
import EditTenantModal from "../../components/tenants/EditTenantModal";
import DeleteTenantModal from "../../components/tenants/DeleteTenantModal";

function Tenants() {

    const [tenants, setTenants] = useState([]);
    const [selectedTenant, setSelectedTenant] = useState(null);
    const [showEditModal, setShowEditModal] = useState(false);
    const [showAddModal, setShowAddModal] = useState(false);
    const [selectedDeleteTenant, setSelectedDeleteTenant] = useState(null);
    const [showDeleteModal, setShowDeleteModal] = useState(false);

    useEffect(() => {
        loadTenants();
    }, []);

    const loadTenants = async () => {

        try {

            const response = await getTenants();

            setTenants(response.data);

        } catch (error) {

            console.log(error);

        }

    };

    return (

        <AdminLayout>

            <div className="d-flex justify-content-between align-items-center mb-4">

                <h2>Tenants</h2>

                <button
                    className="btn btn-primary"
                    onClick={() => setShowAddModal(true)}
                >

                    <i className="bi bi-plus-circle me-2"></i>

                    Add Tenant

                </button>

            </div>

            <div className="card shadow-sm">

                <div className="card-body p-0">

                    <table className="table table-hover mb-0">

                        <thead className="table-light">

                            <tr>

                                <th>ID</th>
                                <th>Name</th>
                                <th>Email</th>
                                <th>Phone</th>
                                <th>Description</th>
                                <th>Slug</th>
                                <th>Support Mail</th>
                                <th>Sender Name</th>
                                <th>Reply-To Mail</th>
                                <th>Status</th>
                                <th>Action</th>
                            </tr>

                        </thead>

                        <tbody>

                            {tenants.map((tenant) => (

                                <tr key={tenant.uuid}>

                                    <td>{tenant.id}</td>

                                    <td>{tenant.name}</td>

                                    <td>{tenant.email}</td>

                                    <td>{tenant.phone}</td>

                                    <td>{tenant.description}</td>

                                    <td>{tenant.slug}</td>

                                    <td>{tenant.support_email} </td>
                                    <td>{tenant.sender_name}</td>
                                    <td>{tenant.reply_to_email}</td>

                                    <td>

                                        <span
                                            className={`badge ${
                                                tenant.is_active
                                                    ? "bg-success"
                                                    : "bg-danger"
                                            }`}
                                        >
                                            {tenant.is_active ? "Active" : "Inactive"}
                                        </span>

                                    </td>

                                    <td>

                                        <button
                                            className="btn btn-warning btn-sm me-2"
                                            onClick={() => {
                                                setSelectedTenant(tenant);
                                                setShowEditModal(true);
                                            }}
                                        >
                                            <i className="bi bi-pencil"></i>
                                        </button>

                                        <button
                                            className="btn btn-danger btn-sm"
                                            onClick={() => {
                                                console.log("Delete clicked");
                                                console.log(tenant);

                                                setSelectedDeleteTenant(tenant);
                                                setShowDeleteModal(true);
                                            }}
                                        >
                                            <i className="bi bi-trash"></i>
                                        </button>

                                    </td>

                                    


                                </tr>

                            ))}

                        </tbody>

                    </table>

                </div>

            </div>
        <AddTenantModal
            show={showAddModal}
            onClose={() => setShowAddModal(false)}
            onSuccess={() => {
                loadTenants();
                setShowAddModal(false);
            }}
        />
        <EditTenantModal
            tenant={selectedTenant}
            show={showEditModal}
            onClose={() => setShowEditModal(false)}
            onSuccess={() => {
                loadTenants();
                setShowEditModal(false);
            }}
        />
        <DeleteTenantModal
            tenant={selectedDeleteTenant}
            show={showDeleteModal}
            onClose={() => setShowDeleteModal(false)}
            onSuccess={() => {
                loadTenants();
                setShowDeleteModal(false);
            }}
        />

        </AdminLayout>

    );

}

export default Tenants;