import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import PlatformLogin from "../pages/auth/PlatformLogin";
import TenantLogin from "../pages/auth/TenantLogin";

import PlatformDashboard from "../pages/dashboard/PlatformDashboard";
import TenantDashboard from "../pages/dashboard/TenantDashboard";

import Tenants from "../pages/tenants/Tenants";
import Agents from "../pages/agents/Agents";

import ProtectedRoute from "../components/ProtectedRoute";

import AssignTenantFeatures from "../pages/rbac/AssignTenantFeatures";

import Dashboard from "../pages/tenants/Dashboard";
import Orders from "../pages/tenants/Orders";
import Tickets from "../pages/tenants/Tickets";
import Customers from "../pages/tenants/Customers";
import Emails from "../pages/tenants/Emails";
import Conversations from "../pages/tenants/Conversations";
import Products from "../pages/tenants/Products";
import TestEmail from "../pages/tenants/TestEmail";

function AppRoutes() {
    return (
        <BrowserRouter>
            <Routes>

                {/* Authentication */}

                <Route path="/" element={<Navigate to="/login" />} />

                <Route path="/login" element={<PlatformLogin />} />

                <Route path="/tenant/login" element={<TenantLogin />} />

                {/* Platform */}

                <Route
                    path="/dashboard"
                    element={
                        <ProtectedRoute allowedRoles={["platform"]}>
                            <PlatformDashboard />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/tenants"
                    element={
                        <ProtectedRoute allowedRoles={["platform"]}>
                            <Tenants />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/agents"
                    element={
                        <ProtectedRoute allowedRoles={["platform"]}>
                            <Agents />
                        </ProtectedRoute>
                    }
                />

                {/* Tenant */}

                <Route
                    path="/tenant/dashboard"
                    element={
                        <ProtectedRoute allowedRoles={["tenant"]}>
                            <TenantDashboard />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/tenant/overview"
                    element={
                        <ProtectedRoute allowedRoles={["tenant"]}>
                            <Dashboard />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/tenant/orders"
                    element={
                        <ProtectedRoute allowedRoles={["tenant"]}>
                            <Orders />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/tenant/tickets"
                    element={
                        <ProtectedRoute allowedRoles={["tenant"]}>
                            <Tickets />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/tenant/customers"
                    element={
                        <ProtectedRoute allowedRoles={["tenant"]}>
                            <Customers />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/tenant/mail-logs"
                    element={
                        <ProtectedRoute allowedRoles={["tenant"]}>
                            <Emails />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/tenant/conversations"
                    element={
                        <ProtectedRoute allowedRoles={["tenant"]}>
                            <Conversations />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/tenant/products"
                    element={
                        <ProtectedRoute allowedRoles={["tenant"]}>
                            <Products />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/tenant/test-mail"
                    element={
                        <ProtectedRoute allowedRoles={["tenant"]}>
                            <TestEmail />
                        </ProtectedRoute>
                    }
                />

                {/* 404 */}

                <Route
                    path="*"
                    element={<h2 className="text-center mt-5">404 Page Not Found</h2>}
                />

                <Route
                    path="/assign-features"
                    element={
                        <ProtectedRoute allowedRoles={["platform"]}>
                            <AssignTenantFeatures />
                        </ProtectedRoute>
                    }
                />

            </Routes>
        </BrowserRouter>
    );
}

export default AppRoutes;