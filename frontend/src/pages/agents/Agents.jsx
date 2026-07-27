import { useEffect, useState } from "react";

import TenantLayout from "../../layouts/TenantLayout";

import {
    getUsers,
    deleteUser,
} from "../../api/userApi";

import AddAgentModal from "../../components/agents/AddAgentModal";
import EditAgentModal from "../../components/agents/EditAgentModal";
import DeleteAgentModal from "../../components/agents/DeleteAgentModal";

function Agents() {

    const [agents, setAgents] = useState([]);

    const [loading, setLoading] = useState(true);

    const [showAdd, setShowAdd] = useState(false);

    const [showEdit, setShowEdit] = useState(false);

    const [showDelete, setShowDelete] = useState(false);

    const [selectedAgent, setSelectedAgent] = useState(null);

    const loadAgents = async () => {

        try {

            setLoading(true);

            const response = await getUsers();

            const users = response.data || [];

            const filteredAgents = users.filter(
                (user) => user.role === "agent"
            );

            setAgents(filteredAgents);

        }

        catch (error) {

            console.error(error);

        }

        finally {

            setLoading(false);

        }

    };

    useEffect(() => {

        loadAgents();

    }, []);

    return (

        <TenantLayout>

            <div className="d-flex justify-content-between align-items-center mb-4">

                <h2>Agents</h2>

                <button
                    className="btn btn-primary"
                    onClick={() => setShowAdd(true)}
                >
                    <i className="bi bi-plus-circle me-2"></i>

                    Add Agent
                </button>

            </div>

            <table className="table table-bordered table-hover align-middle">

                <thead className="table-dark">

                    <tr>

                        <th>First Name</th>

                        <th>Last Name</th>

                        <th>Email</th>

                        <th>Role</th>

                        <th>Status</th>

                        <th width="180">Actions</th>

                    </tr>

                </thead>

                <tbody>

                    {loading ? (

                        <tr>

                            <td
                                colSpan="6"
                                className="text-center"
                            >
                                Loading...
                            </td>

                        </tr>

                    ) : agents.length === 0 ? (

                        <tr>

                            <td
                                colSpan="6"
                                className="text-center"
                            >
                                No Agents Found
                            </td>

                        </tr>

                    ) : (

                        agents.map((agent) => (

                            <tr key={agent.uuid}>

                                <td>{agent.first_name}</td>

                                <td>{agent.last_name}</td>

                                <td>{agent.email}</td>

                                <td>{agent.role}</td>

                                <td>

                                    {agent.is_active ? (

                                        <span className="badge bg-success">
                                            Active
                                        </span>

                                    ) : (

                                        <span className="badge bg-danger">
                                            Inactive
                                        </span>

                                    )}

                                </td>

                                <td>

                                    <button
                                        className="btn btn-warning btn-sm me-2"
                                        onClick={() => {

                                            setSelectedAgent(agent);

                                            setShowEdit(true);

                                        }}
                                    >
                                        Edit
                                    </button>

                                    <button
                                        className="btn btn-danger btn-sm"
                                        onClick={() => {

                                            setSelectedAgent(agent);

                                            setShowDelete(true);

                                        }}
                                    >
                                        Delete
                                    </button>

                                </td>

                            </tr>

                        ))

                    )}

                </tbody>

            </table>

            <AddAgentModal

                show={showAdd}

                onClose={() => setShowAdd(false)}

                onSuccess={() => {

                    setShowAdd(false);

                    loadAgents();

                }}

            />

            <EditAgentModal

                show={showEdit}

                agent={selectedAgent}

                onClose={() => setShowEdit(false)}

                onSuccess={() => {

                    setShowEdit(false);

                    loadAgents();

                }}

            />

            <DeleteAgentModal

                show={showDelete}

                agent={selectedAgent}

                onClose={() => setShowDelete(false)}

                onSuccess={() => {

                    setShowDelete(false);

                    loadAgents();

                }}

            />

        </TenantLayout>

    );

}

export default Agents;