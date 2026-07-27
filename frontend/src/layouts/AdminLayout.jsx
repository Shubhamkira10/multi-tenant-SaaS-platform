import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";

function AdminLayout({ children }) {
    return (
        <div className="d-flex">

            <Sidebar role="platform" />

            <div className="flex-grow-1 bg-light min-vh-100">

                <Navbar />

                <main className="container-fluid p-4">
                    {children}
                </main>

            </div>

        </div>
    );
}

export default AdminLayout;