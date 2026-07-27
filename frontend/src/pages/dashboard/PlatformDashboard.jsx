import AdminLayout from "../../layouts/AdminLayout";

function Dashboard() {

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

                            <h2>1</h2>

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