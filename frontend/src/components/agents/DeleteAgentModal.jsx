import { deleteUser } from "../../api/userApi";

function DeleteAgentModal({
    show,
    agent,
    onClose,
    onSuccess,
}) {

    if (!show || !agent) return null;

    const handleDelete = async () => {

        try {

            await deleteUser(agent.uuid);

            onSuccess();

        }

        catch (error) {

            console.error(error);

            alert(
                error?.response?.data?.message ||
                "Unable to delete agent."
            );

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
                            Delete Agent
                        </h5>

                        <button
                            className="btn-close"
                            onClick={onClose}
                        ></button>

                    </div>

                    <div className="modal-body">

                        <p>
                            Are you sure you want to delete this agent?
                        </p>

                        <div className="alert alert-warning mb-0">

                            <strong>Name:</strong>{" "}
                            {agent.first_name} {agent.last_name}

                            <br />

                            <strong>Email:</strong>{" "}
                            {agent.email}

                        </div>

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

export default DeleteAgentModal;