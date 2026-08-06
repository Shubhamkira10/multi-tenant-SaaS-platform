import { useCallback } from "react";
import usePolling from "../../hooks/usePolling";
import { fetchPlatformDashboard } from "../../api/dashboardApi";
import AdminLayout from "../../layouts/AdminLayout";

function Dashboard() {

    const getData = useCallback(
        () => fetchPlatformDashboard(),
        []
    );

    const {
        data,
        loading,
    } = usePolling(getData, 5000);

    return (
        <AdminLayout>

            <h2 className="mb-4">
                Dashboard
            </h2>

            <div className="row">

                <div className="col-md-3">
                    <div className="card shadow-sm">
                        <div className="card-body">
                            <h6>Total Tenants</h6>
                            <h2>
                                {loading ? "..." : data?.total_tenants ?? 0}
                            </h2>
                        </div>
                    </div>
                </div>

                <div className="col-md-3">
                    <div className="card shadow-sm">
                        <div className="card-body">
                            <h6>Total Users</h6>
                            <h2>0</h2>
                        </div>
                    </div>
                </div>

                <div className="col-md-3">
                    <div className="card shadow-sm">
                        <div className="card-body">
                            <h6>Total Agents</h6>
                            <h2>0</h2>
                        </div>
                    </div>
                </div>

                <div className="col-md-3">
                    <div className="card shadow-sm">
                        <div className="card-body">
                            <h6>Total Interns</h6>
                            <h2>0</h2>
                        </div>
                    </div>
                </div>

            </div>

        </AdminLayout>
    );
}

export default Dashboard;