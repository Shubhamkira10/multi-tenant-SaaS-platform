import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";

function TenantLayout({ children }) {
    return (
        <div
            className="d-flex"
            style={{
                minHeight: "100vh",
                overflow: "hidden",
            }}
        >
            <Sidebar role="tenant" />

            <div
                className="flex-grow-1 d-flex flex-column"
                style={{
                    minWidth: 0,
                    overflow: "hidden",
                }}
            >
                <Navbar />

                <main
                    className="flex-grow-1 p-4"
                    style={{
                        overflow: "auto",
                    }}
                >
                    {children}
                </main>
            </div>
        </div>
    );
}

export default TenantLayout;