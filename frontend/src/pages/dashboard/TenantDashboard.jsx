import TenantLayout from "../../layouts/TenantLayout";

function TenantDashboard() {

    return (

        <TenantLayout>

            <div className="container-fluid">

                <div className="mb-4">

                    <h2>Tenant Dashboard</h2>

                    <p className="text-muted">
                        Welcome to the Tenant Management Panel
                    </p>

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