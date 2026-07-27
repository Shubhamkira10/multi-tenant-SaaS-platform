import { deleteTenant } from "../../api/tenantApi";

function DeleteTenantModal({
    tenant,
    show,
    onClose,
    onSuccess,
}) {

    if (!show || !tenant) return null;

    const handleDelete = async () => {

        try {

            await deleteTenant(tenant.uuid);

            onSuccess();

        } catch (error) {

            console.log(error.response?.data);

        }

    };

    return (

        <div
            className="modal d-block"
            tabIndex="-1"
            style={{ backgroundColor: "rgba(0,0,0,0.5)" }}
        >

            <div className="modal-dialog modal-dialog-centered">

                <div className="modal-content">

                    <div className="modal-header">

                        <h5 className="modal-title text-danger">

                            Delete Tenant

                        </h5>

                        <button
                            type="button"
                            className="btn-close"
                            onClick={onClose}
                        />

                    </div>

                    <div className="modal-body">

                        <p>

                            Are you sure you want to delete

                            <strong> {tenant.name}</strong>?

                        </p>

                        <p className="text-danger mb-0">

                            This action cannot be undone.

                        </p>

                    </div>

                    <div className="modal-footer">

                        <button
                            className="btn btn-secondary"
                            onClick={onClose}
                        >
                            Cancel
                        </button>

                        <button
                            className="btn btn-danger"
                            onClick={handleDelete}
                        >
                            Delete
                        </button>

                    </div>

                </div>

            </div>

        </div>

    );

}

export default DeleteTenantModal;